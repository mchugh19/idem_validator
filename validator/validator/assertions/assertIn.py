def check(hub, output, expected, print_result):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    if output is None:
        return "Fail: Module output is None"
    try:
        if print_result:
            assert expected in output, f"{expected} not found in {output}"
        else:
            assert expected in output, "Result not found"
    except AssertionError as err:
        result = f"Fail: {err}"
    except TypeError as err:
        result = "Fail: Result not found"
    return result
