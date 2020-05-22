def check(hub, output, expected, print_result):
    result = "Pass"
    if not expected:
        return "Fail: Missing expected input"
    try:
        if print_result:
            assert float(expected) >= float(
                output
            ), f"{float(expected)} is not >= {float(output)}"
        else:
            assert float(expected) >= float(
                output
            ), "Result is not greater than or equal to"
    except (AssertionError, ValueError) as err:
        result = f"Fail: {err}"
    except TypeError:
        result = f"Fail: Unexpected None input"
    return result
