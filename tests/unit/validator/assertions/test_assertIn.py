import validator.validator.assertions.assertIn as assertIn

def test_assertIn_is_in(mock_hub):
    print_result = True
    output = "something"
    expected = "thing"
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    output = "something"
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

def test_assertIn_not_in(mock_hub):
    output = "something"
    expected = None
    print_result = True
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
    expected = "notin"
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} not found in something"
    expected = True
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result not found"
    expected = 10
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result not found"

def test_assertIn_not_in_no_print(mock_hub):
    print_result = False
    output = "something"
    expected = "notin"
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result not found"

def test_assertIn_empty_inputs(mock_hub):
    print_result = True

    output = None
    expected = "notin"
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"

    output = "something"
    expected = None
    result = assertIn.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
