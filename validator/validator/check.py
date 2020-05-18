from typing import Dict
import os
import time


def _generate_result_summary(hub):
    """
    generate and append test summary output
    """
    passed = 0
    failed = 0
    skipped = 0
    total_time = 0.0
    for key, value in hub.validator.RUNS.items():
        if value["status"].startswith("Pass"):
            passed = passed + 1
        if value["status"].startswith("Fail"):
            failed = failed + 1
        if value["status"].startswith("Skip"):
            skipped = skipped + 1
        total_time = total_time + float(value["duration"])
    hub.validator.RUNS.update(
        {
            "TEST RESULTS": {
                "Execution Time": round(total_time, 4),
                "Passed": passed,
                "Failed": failed,
                "Skipped": skipped,
            }
        }
    )

def _get_tst_files(hub) -> Dict:
    '''
    Find specified file and path
    '''
    tst_sources = []
    tsts = []
    for tst in hub.OPT["validator"]["tests"]:
        if os.path.isfile(tst):
            if tst.endswith('.tst'):
                ref = tst[:-4]
                tsts.append(ref)
            tst_dir = os.path.dirname(tst)
            implied = f"file://{tst_dir}"
            if implied not in tst_sources:
                tst_sources.append(implied)
        else:
            tsts.append(tst)
    return {"tst_sources": tst_sources, "tsts": tsts}


def _assert_block(hub, test_name, test_block) -> Dict:
    expected_return = test_block.get('expected_return', None)
    assertion_section = test_block.get("assertion_section", None)
    assertion_section_delimiter = test_block.get(
        "assertion_section_delimiter", hub.OPT['validator']['delimiter']
    )
    if assertion_section:
        test_output = hub.validator.utils.traverse_dict_and_list(hub.validator.RUNS[test_name]['execution_output'], assertion_section, delimiter=assertion_section_delimiter)
    else:
        test_output = hub.validator.RUNS[test_name]['execution_output']
    assert_result = getattr(hub.validator.assertions, test_block["assertion"]).check(test_output, expected_return)
    return assert_result


def _run_assertions(
        hub,
        test_name: str,
        test_data: Dict
    ):
        """
        Run assertion against input
        """
        if "assertions" in test_data:
            for num, assert_group in enumerate(test_data.get("assertions"), start=1):
                assert_result = _assert_block(hub, test_name, assert_group)
                hub.validator.RUNS[test_name][f'assertion{num}'] = {}
                hub.validator.RUNS[test_name][f'assertion{num}']['status'] = assert_result
            # Walk individual assert status results to set the top level status
            # key as needed
            for k, v in hub.validator.RUNS[test_name].items():
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
            hub.validator.RUNS[test_name]['status'] = assert_result


async def _execute(hub, test_block: Dict):
    for test_name, test_content in test_block.items():
        start = time.time()
        hub.validator.RUNS[test_name] = {}
        args = test_content.get('args', [])
        kwargs = test_content.get('kwargs', {})
        if args:
            test_result = await getattr(hub.exec, test_content['module_and_function'])(args, **kwargs)
        else:
            test_result = await getattr(hub.exec, test_content['module_and_function'])(**kwargs)
        hub.validator.RUNS[test_name]['execution_output'] = test_result

        # Run assertion against exec output
        _run_assertions(hub, test_name, test_content)
        end = time.time()
        hub.validator.RUNS[test_name]["duration"] = round(end - start, 4)
        # Delete execution results from hub data
        del hub.validator.RUNS[test_name]['execution_output']


async def run_test(hub) -> Dict:
    src = _get_tst_files(hub)
    blocks = hub.rend.init.blocks(f'{src["tsts"][0]}.tst')
    for bname, block in blocks.items():
        tests = await hub.rend.init.parse_bytes(
                    block, hub.OPT["validator"]["render"]
                )
        for test_name in tests:
            await _execute(hub, {test_name: tests[test_name]})
    _generate_result_summary(hub)
    print(hub.output.pretty.display(hub.validator.RUNS))
