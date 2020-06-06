import validator.validator.assertions.assertGreater as assertGreater


def test_assertGreater_greater(mock_hub):
    expected = 5
    output = 4

    print_result = False
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    print_result = True
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertGreater_other_no_print(mock_hub):
    expected = 5
    print_result = False

    output = 5
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not greater"
    output = 6
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not greater"
    output = ""
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "10"
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not greater"
    output = True
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertGreater_other_print(mock_hub):
    expected = 5
    print_result = True

    output = 6
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 5.0 is not greater than 6.0"
    output = ""
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    output = "thing"
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{output}'"
    output = None
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
    output = "10"
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: 5.0 is not greater than 10.0"
    output = True
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"
    output = False
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is a boolean"


def test_assertGreater_bad_assert_value_print(mock_hub):
    output = 6
    print_result = True

    expected = ""
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: "
    expected = "thing"
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: could not convert string to float: '{expected}'"
    expected = None
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
    expected = True
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
    expected = False
    result = assertGreater.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Assertion value is a boolean"
