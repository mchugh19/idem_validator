import validator.validator.assertions.assertEmpty as assertEmpty

def test_assertEmpty_empty(mock_hub):
    expected = None
    print_result = True
    output = ""
    result = assertEmpty.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    output = None
    result = assertEmpty.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

def test_assertEmpty_not_empty(mock_hub):
    output = "something"
    expected = None
    print_result = True
    result = assertEmpty.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {output} is not empty"

def test_assertEmpty_not_empty_no_print(mock_hub):
    output = "something"
    expected = None
    print_result = False
    result = assertEmpty.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not empty"
