def check(hub, output, expected, print_result: bool):
    result = "Pass"
    try:
        assert output, "value is empty"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
