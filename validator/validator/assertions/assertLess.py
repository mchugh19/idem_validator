def check(hub, output, expected, print_result):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    try:
        if print_result:
            assert float(expected) < float(
                output
            ), f"{float(expected)} is not less than {float(output)}"
        else:
            assert float(expected) < float(output), "Result is not less"
    except (AssertionError, ValueError) as err:
        result = f"Fail: {err}"
    except TypeError:
        result = f"Fail: Unexpected None input"
    return result
