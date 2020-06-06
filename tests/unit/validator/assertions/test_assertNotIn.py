import validator.validator.assertions.assertNotIn as assertNotIn


def test_assertNotIn_not_in(mock_hub):
    print_result = True
    output = "something"
    expected = "notin"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = True
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = 10
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = "10"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertNotIn_is_in(mock_hub):
    print_result = True

    output = "something"
    expected = "thing"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} found"


def test_assertNotIn_in_no_print(mock_hub):
    print_result = False

    output = "something"
    expected = "thing"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result found"


def test_assertNotIn_empty_inputs(mock_hub):
    print_result = True

    output = None
    expected = "notin"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"

    expected = None
    output = "something"
    result = assertNotIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
