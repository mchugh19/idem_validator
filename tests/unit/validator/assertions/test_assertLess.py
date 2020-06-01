import validator.validator.assertions.assertLess as assertLess

def test_assertLess_greater(mock_hub):
    expected = 5
    print_result = False

    output = 6
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    print_result = True
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertLess_other_no_print(mock_hub):
    expected = 7
    print_result = False

    output = 7
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not less"
    output = 6
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not less"
    output = ""
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "6"
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not less"
    output = True
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"

def test_assertLess_other_print(mock_hub):
    expected = 7
    print_result = True

    output = 7
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 7.0 is not less than 7.0"
    output = 6
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 7.0 is not less than 6.0"
    output = ""
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "6"
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 7.0 is not less than 6.0"
    output = True
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertLess_bad_assert_value_print(mock_hub):
    output = 6
    print_result = True

    expected = ""
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    expected = "thing"
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{expected}'"
    expected = None
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
    expected = True
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
    expected = False
    result = assertLess.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
