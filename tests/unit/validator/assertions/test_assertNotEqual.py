import validator.validator.assertions.assertNotEqual as assertNotEqual


def test_assertNotEqual_not_equal(mock_hub):
    print_result = True
    output = "something"
    expected = "notin"
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = 10
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = False
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    expected = ""
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertNotEqual_is_equal(mock_hub):
    output = "something"
    print_result = True
    expected = "something"
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: Result is equal"
    print_result = False
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: Result is equal"


def test_assertNotEqual_empty_inputs(mock_hub):
    print_result = True

    output = None
    expected = "notin"
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"

    output = "something"
    expected = None
    result = assertNotEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
