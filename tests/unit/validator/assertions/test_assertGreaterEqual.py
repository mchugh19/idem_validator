import validator.validator.assertions.assertGreaterEqual as assertGreaterEqual


def test_assertGreaterEqual_greater(mock_hub):
    expected = 5
    print_result = False

    output = 5
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    output = 4
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    print_result = True
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertGreaterEqual_other_no_print(mock_hub):
    expected = 5
    print_result = False

    output = 6
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not greater than or equal to"
    output = ""
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "10"
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not greater than or equal to"
    output = True
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertGreaterEqual_other_print(mock_hub):
    expected = 5
    print_result = True

    output = 6
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 5.0 is not >= 6.0"
    output = ""
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "10"
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 5.0 is not >= 10.0"
    output = True
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertGreaterEqual_bad_assert_value_print(mock_hub):
    output = 6
    print_result = True

    expected = ""
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    expected = "thing"
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{expected}'"
    expected = None
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
    expected = True
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
    expected = False
    result = assertGreaterEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
