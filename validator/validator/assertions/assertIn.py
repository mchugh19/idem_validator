def check(hub, output, expected):
    result = "Pass"
    try:
        assert expected in output, "Result not found"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
