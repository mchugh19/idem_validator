def check(hub, output, expected, print_result):
    result = "Pass"
    try:
        if print_result:
            assert expected not in output, f"{output} found"
        else:
            assert expected not in output, "Result found"
    except AssertionError as err:
        result = f"Fail: {err}"
    except TypeError as err:
        # If output is none expected isn't found so test passes
        pass
    return result
