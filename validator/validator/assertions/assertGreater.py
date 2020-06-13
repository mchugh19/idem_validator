def check(hub, output, expected, print_result: bool):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    if output is None:
        return "Fail: Module output is None"
    if isinstance(output, bool):
        return "Fail: Module output is a boolean"
    if isinstance(expected, bool):
        return "Fail: Assertion value is a boolean"
    try:

        if print_result:
            assert float(expected) > float(
                output
            ), f"{float(expected)} is not greater than {float(output)}"
        else:
            assert float(expected) > float(output), "Result is not greater"
    except (AssertionError, ValueError) as err:
        result = f"Fail: {err}"
    return result
