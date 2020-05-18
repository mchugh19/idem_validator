def check(hub, output, expected):
    result = "Pass"
    try:
        assert output is False, "value is not False"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
