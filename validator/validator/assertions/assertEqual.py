def check(hub, output, expected):
    result = "Pass"
    try:
        assert expected == output, "Result is not equal"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
