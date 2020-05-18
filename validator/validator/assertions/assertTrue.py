def check(hub, output, expected):
    result = "Pass"
    try:
        assert output is True, "value is not True"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
