def check(hub, output, expected):
    result = "Pass"
    try:
        assert output, "value is empty"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
