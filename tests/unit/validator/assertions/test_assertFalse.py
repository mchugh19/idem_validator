import validator.validator.assertions.assertFalse as assertFalse

def test_assertFalse_false(mock_hub):
    expected = None
    print_result = True

    output = False
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    output = "false"
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    output = "False"
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_asserFalse_other(mock_hub):
    expected = None
    print_result = False

    output = "something"
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is not False"
    output = True
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is not False"
    output = "no"
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is not False"
    output = "0"
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is not False"
    output = 0
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: value is not False"
    output = None
    result = assertFalse.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"
