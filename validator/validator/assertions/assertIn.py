def check(hub, output, expected, print_result):
    result = "Pass"
    if not expected:
        return "Fail: Missing expected input"
    try:
        if print_result:
            assert expected in output, f"{expected} not found in {output}"
        else:
            assert expected in output, "Result not found"
    except AssertionError as err:
        result = f"Fail: {err}"
    except TypeError as err:
        if print_result:
            result = f"Fail: {expected} not found in None"
        else:
            result = "Fail: Result not found"
    return result
