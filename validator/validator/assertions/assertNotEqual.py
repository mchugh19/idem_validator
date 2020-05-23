def check(hub, output, expected, print_result):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    try:
        assert expected != output, "Result is equal"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
