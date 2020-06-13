def check(hub, output, expected, print_result: bool):
    result = "Pass"
    if expected is None:
        return "Fail: Missing expected input"
    if output is None:
        return "Fail: Module output is None"
    try:
        if print_result:
            assert expected not in output, f"{expected} found"
        else:
            assert expected not in output, "Result found"
    except AssertionError as err:
        result = f"Fail: {err}"
    except TypeError as err:
        # If output is none expected isn't found so test passes
        pass
    return result
