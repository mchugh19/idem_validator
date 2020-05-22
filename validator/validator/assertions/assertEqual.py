def check(hub, output, expected, print_result):
    result = "Pass"
    if not expected:
        return "Fail: Missing expected input"
    try:
        if print_result:
            assert expected == output, f"{expected} is not equal to {output}"
        else:
            assert expected == output, "Result is not equal"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
