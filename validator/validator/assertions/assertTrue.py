def check(hub, output, expected, print_result: bool):
    result = "Pass"
    if output is None:
        return "Fail: Module output is None"
    try:
        if isinstance(output, str) and output.lower() in ["true"]:
            output = True
        assert output is True, "value is not True"
    except AssertionError as err:
        result = f"Fail: {err}"
    return result
