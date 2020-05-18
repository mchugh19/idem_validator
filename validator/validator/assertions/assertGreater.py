def check(hub, output, expected):
    result = "Pass"
    try:
        assert expected > output, "Result is not greater"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
