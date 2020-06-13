def check(hub, output, expected, print_result: bool):
    result = "Pass"
    try:
        if print_result:
            assert not output, f"{output} is not empty"
        else:
            assert not output, "value is not empty"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
