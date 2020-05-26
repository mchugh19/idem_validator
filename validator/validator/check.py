from typing import Dict
import os
import time
import inspect
import copy
import sys
import asyncio


def _generate_result_summary(hub) -> None:
    """
    generate and append test summary output
    """
    passed = 0
    failed = 0
    skipped = 0
    for key, value in hub.validator.RUNS.items():
        if value["status"].startswith("Pass"):
            passed = passed + 1
        if value["status"].startswith("Fail"):
            failed = failed + 1
        if value["status"].startswith("Skip"):
            skipped = skipped + 1
    hub.validator.RUNS.update(
        {"TEST RESULTS": {"Passed": passed, "Failed": failed, "Skipped": skipped,}}
    )


def _assert_block(hub, test_name: str, test_block: Dict) -> Dict:
    """
    Runs actual assertion modules against test output
    Expected to be called for a single assertion or a loop of assertions
    """
    expected_return = test_block.get("expected_return", None)
    assertion_section = test_block.get("assertion_section", None)
    assertion_section_delimiter = test_block.get(
        "assertion_section_delimiter", hub.OPT["validator"]["delimiter"]
    )
    if not assertion_section_delimiter:
        hub.log.error(
            f"Invalid assertion delimiter {test_block['assertion_section_delimiter']}"
        )
        return f"Fail: Invalid assertion delimiter {test_block['assertion_section_delimiter']}"
    assert_print_result = test_block.get("print_result", True)
    if assertion_section:
        test_output = hub.validator.utils.traverse_dict_and_list(
            hub.validator.RUNS[test_name]["execution_output"],
            assertion_section,
            delimiter=assertion_section_delimiter,
        )
    else:
        test_output = hub.validator.RUNS[test_name]["execution_output"]
    try:
        assert_result = getattr(
            hub.validator.assertions, test_block["assertion"]
        ).check(test_output, expected_return, assert_print_result)
    except AttributeError:
        hub.log.error(f"Invalid assertion {test_block['assertion']}")
        return f"Fail: Invalid assertion {test_block['assertion']}"
    except KeyError:
        hub.log.error(f'Test "{test_name}" missing assertion for {test_block}')
        return f'Fail: Test "{test_name}" missing assertion for {test_block}'
    return assert_result


def _run_assertions(hub, test_name: str, test_data: Dict) -> None:
    """
    Process the test data to call single assertion or loop over assertions
    Set the assertion status as approperate
    """
    if "assertions" in test_data:
        for num, assert_group in enumerate(test_data.get("assertions"), start=1):
            assert_result = _assert_block(hub, test_name, assert_group)
            hub.validator.RUNS[test_name][f"assertion{num}"] = {}
            hub.validator.RUNS[test_name][f"assertion{num}"]["status"] = assert_result
        # Walk individual assert status results to set the top level status
        # key as needed
        for k, v in copy.copy(hub.validator.RUNS[test_name]).items():
            if k.startswith("assertion"):
                for assert_k, assert_v in hub.validator.RUNS[test_name][k].items():
                    if assert_k.startswith("status"):
                        if hub.validator.RUNS[test_name][k][assert_k] != "Pass":
                            hub.validator.RUNS[test_name]["status"] = "Fail"
                            break
        if not hub.validator.RUNS[test_name].get("status"):
            hub.validator.RUNS[test_name]["status"] = "Pass"
    else:
        assert_result = _assert_block(hub, test_name, test_data)
        hub.validator.RUNS[test_name]["status"] = assert_result


async def execute(hub) -> None:
    """
    Worker called as a task to pop a message off the queue and process it
    """
    while True:
        test_block = await hub.validator.INQUE.get()
        hub.log.debug(f"Worker running for {test_block}")
        for test_name, test_content in test_block.items():
            hub.validator.RUNS[test_name] = {}
            skip = test_content.get("skip", False)
            if skip:
                hub.validator.RUNS[test_name]["duration"] = 0.0
                hub.validator.RUNS[test_name]["status"] = "Skip"
                hub.validator.INQUE.task_done()
                break
            start = time.monotonic()
            args = test_content.get("args", [])
            kwargs = test_content.get("kwargs", {})
            try:
                if args:
                    test_result = getattr(
                        hub.exec, test_content["module_and_function"]
                    )(args, **kwargs)
                else:
                    test_result = getattr(
                        hub.exec, test_content["module_and_function"]
                    )(**kwargs)
                if inspect.iscoroutine(test_result):
                    test_result = await test_result
                hub.validator.RUNS[test_name]["execution_output"] = test_result
                # Run assertion against exec output
                _run_assertions(hub, test_name, test_content)
            except AttributeError:
                hub.validator.RUNS[test_name][
                    "status"
                ] = f"Fail: Invalid module_and_function {test_content['module_and_function']}"
                hub.log.error(
                    f"Invalid module_and_function {test_content['module_and_function']}"
                )
            except (FileNotFoundError, SystemError):
                hub.validator.RUNS[test_name][
                    "status"
                ] = f"Fail: Error running {test_content['module_and_function']} {args} {kwargs}"
                hub.log.error(
                    f"Fail: Error running {test_content['module_and_function']} {args} {kwargs}"
                )
            except:
                hub.validator.RUNS[test_name][
                    "status"
                ] = f"Fail: Error running {test_name} {sys.exc_info()[0]}"
                hub.log.error(
                    f"Fail: Error running {test_name}"
                )
            end = time.monotonic()
            hub.validator.RUNS[test_name]["duration"] = round(end - start, 4)
            # Delete execution results from hub data
            hub.validator.RUNS[test_name].pop("execution_output", None)
            hub.validator.INQUE.task_done()


async def main(hub) -> None:
    """
    Gather test files, process them through rend.
    Put the results into a queue then call workers to run exec modules and assert on results
    Output results through rend output, and exit 1 if failures detected
    """
    hub.validator.INQUE = asyncio.Queue()
    start = time.monotonic()
    for tst in hub.OPT["validator"]["tests"]:
        blocks = hub.rend.init.blocks(tst)
        for bname, block in blocks.items():
            tests = await hub.rend.init.parse_bytes(
                block, hub.OPT["validator"]["render"]
            )
            if tests:
                for test_name in tests:
                    hub.validator.INQUE.put_nowait({test_name: tests[test_name]})
    workers = []
    for _ in range(int(hub.OPT["validator"]["workers"])):
        workers.append(asyncio.create_task(hub.validator.check.execute()))
    await hub.validator.INQUE.join()

    # Cleanup worker tasks
    for task in workers:
        task.cancel()

    _generate_result_summary(hub)
    end = time.monotonic()
    hub.validator.RUNS["TEST RESULTS"]["Execution Time"] = round(end - start, 4)
    print(
        getattr(hub.output, hub.OPT["validator"]["output"]).display(hub.validator.RUNS)
    )
    if hub.validator.RUNS["TEST RESULTS"]["Failed"] > 0:
        sys.exit(1)
