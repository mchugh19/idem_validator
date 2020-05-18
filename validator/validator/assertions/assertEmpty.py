def check(hub, output, expected):
    result = "Pass"
    try:
        assert not output, "value is not empty"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
