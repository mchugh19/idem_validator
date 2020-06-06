import validator.validator.check as check
from mock import patch
import pytest


def test_output_content(hub):
    """
    test that output appends summary information as expected
    """
    runs = {
        "pass 1": {"status": "Pass", "duration": 0.0077},
        "multiple assertion pass test": {
            "assertion1": {"status": "Pass"},
            "assertion2": {"status": "Pass"},
            "status": "Pass",
            "duration": 0.0059,
        },
        "test skip": {"duration": 0.0, "status": "Skip"},
        "fail 1": {"status": "Fail: some reason", "duration": 0.0001},
    }
    hub.validator.RUNS = runs.copy()
    runs.update({"TEST RESULTS": {"Passed": 2, "Failed": 1, "Skipped": 1,}})
    check._generate_result_summary(hub)
    assert hub.validator.RUNS == runs


def test_output_empty(hub):
    """
    test output for empty test runs
    """
    check._generate_result_summary(hub)
    assert hub.validator.RUNS == {
        "TEST RESULTS": {"Failed": 0, "Passed": 0, "Skipped": 0}
    }


@pytest.mark.skip(reason="hub.OPT currently broken")
def test_assert_block(mock_hub):
    test_name = "a test"
    test_dict = {"assertion": "assertThing", "expected_return": "stuff"}
    mock_hub.validator.RUNS = {test_name: {"execution_output": "stuff"}}
    result = check._assert_block(mock_hub, test_name, test_dict)
    # assert result == "Pass"
    # mock_hub.validator.assertions.assertEqual.assert_called_with("boop")
