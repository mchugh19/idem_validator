import validator.validator.assertions.assertNotEmpty as assertNotEmpty


def test_assertNotEmpty_empty(mock_hub):
    expected = None
    print_result = True

    output = ""
    result = assertNotEmpty.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is empty"
    output = None
    result = assertNotEmpty.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is empty"


def test_assertNotEmpty_print_false(mock_hub):
    output = ""
    expected = None
    print_result = False
    result = assertNotEmpty.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is empty"


def test_assertNotEmpty_not_empty(mock_hub):
    output = "something"
    expected = None
    print_result = False
    result = assertNotEmpty.check(mock_hub, output, expected, print_result)
    assert result == f"Pass"
