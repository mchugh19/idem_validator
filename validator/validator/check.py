from typing import Dict, List
import os


def _generate_out_list(results) -> List[Dict]:
    """
    generate test results output list
    """
    passed = 0
    failed = 0
    skipped = 0
    missing_tests = 0
    total_time = 0.0
    for state in results:
        if not results[state].items():
            missing_tests = missing_tests + 1
        else:
            for dummy, val in results[state].items():
                log.info("dummy=%s, val=%s", dummy, val)
                if val["status"].startswith("Pass"):
                    passed = passed + 1
                if val["status"].startswith("Fail"):
                    failed = failed + 1
                if val["status"].startswith("Skip"):
                    skipped = skipped + 1
                total_time = total_time + float(val["duration"])
    out_list = []
    for key, value in results.items():
        out_list.append({key: value})
    out_list = sorted(out_list, key=lambda x: sorted(x.keys()))
    out_list.append(
        {
            "TEST RESULTS": {
                "Execution Time": round(total_time, 4),
                "Passed": passed,
                "Failed": failed,
                "Skipped": skipped,
                "Missing Tests": missing_tests,
            }
        }
    )
    return out_list

def get_tst_files(hub):
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

def create():
    hub.validator.RUNS[name] = {}


async def run_test(hub) -> List[Dict]:
    src = hub.validator.check.get_tst_files()
    #print(src)

    blocks = hub.rend.init.blocks(f'{src["tsts"][0]}.tst')
    for bname, block in blocks.items():
        tests = await hub.rend.init.parse_bytes(
                    block, 'jinja|yaml'
                )
        print(hub.output.pretty.display(tests))
        for test_name, test in tests.items():
            print(hub.output.pretty.display(test))
            args = test.get('args', [])
            kwargs = test.get('kwargs', {})
            test_result = await getattr(hub.exec, test['module_and_function'])(args, **kwargs)
            print(f'XXX got cmd.run result {test_result}')
            pass



    #rendered = await hub.rend.init.parse(f'{src["tsts"][0]}.tst', 'jinja|yaml')
    #print(rendered)

    #return _generate_out_list({})
