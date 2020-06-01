def check(hub, output, expected, print_result):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    if output is None:
        return "Fail: Module output is None"
    try:
        if print_result:
            assert expected == output, f"{expected} is not equal to {output}"
        else:
            assert expected == output, "Result is not equal"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
