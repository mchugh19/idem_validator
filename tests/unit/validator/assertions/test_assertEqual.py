import validator.validator.assertions.assertEqual as assertEqual

def test_assertEqual_is_equal(mock_hub):
    print_result = True
    output = "something"
    expected = "something"
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"

    output = "something\n"
    expected = "something\n"
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Pass"


def test_assertEqual_not_equal(mock_hub):
    output = "something"
    print_result = True
    expected = "notin"
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} is not equal to {output}"
    expected = True
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} is not equal to {output}"
    expected = 10
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} is not equal to {output}"
    expected = ""
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: {expected} is not equal to {output}"

def test_assertEqual_not_equal_no_print(mock_hub):
    output = "something"
    print_result = False
    expected = "notin"
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not equal"
    expected = True
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not equal"
    expected = 10
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not equal"
    expected = ""
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Result is not equal"

def test_assertEqual_empty_inputs(mock_hub):
    print_result = True

    output = None
    expected = "notin"
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Module output is None"

    output = "something"
    expected = None
    result = assertEqual.check(mock_hub, output, expected, print_result)
    assert result == "Fail: Missing expected input"
