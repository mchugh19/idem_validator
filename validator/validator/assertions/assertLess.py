def check(hub, output, expected):
    result = "Pass"
    try:
        assert expected < output, "Result is less"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
