def check(hub, output, expected, print_result):
    result = "Pass"
    if output is None:
        return "Fail: Module output is None"
    try:
        if isinstance(output, str) and output.lower() in ['false']:
            output = False
        assert output is False, "value is not False"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
