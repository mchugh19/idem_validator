import validator.validator.assertions.assertLessEqual as assertLessEqual


def test_assertLessEqual_greater(mock_hub):
    expected = 5
    print_result = False

    output = 6
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    output = 5
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    print_result = True
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertLessEqual_other_no_print(mock_hub):
    expected = 7
    print_result = False

    output = 6
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not less than or equal to"
    output = ""
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "6"
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not less than or equal to"
    output = True
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertLessEqual_other_print(mock_hub):
    expected = 7
    print_result = True

    output = 6
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 7.0 is not <= 6.0"
    output = ""
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "6"
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 7.0 is not <= 6.0"


def test_assertLessEqual_bad_assert_value_print(mock_hub):
    output = 6
    print_result = True

    expected = ""
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    expected = "thing"
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{expected}'"
    expected = None
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
    expected = True
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
    expected = False
    result = assertLessEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
