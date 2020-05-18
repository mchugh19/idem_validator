def check(hub, output, expected):
    result = "Pass"
    try:
        assert expected not in output, "Result found"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
