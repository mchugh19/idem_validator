import validator.validator.assertions.assertTrue as assertTrue


def test_assertTrue_true(mock_hub):
    expected = None
    print_result = True

    output = True
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    output = "true"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == "Pass"
    output = "True"


def test_assertTrue_other(mock_hub):
    expected = None
    print_result = False

    output = "something"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = False
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = "yes"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = "y"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = "1"
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = 1
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: value is not True"
    output = None
    result = assertTrue.check(mock_hub, output, expected, print_result)
    assert result == f"Fail: Module output is None"
