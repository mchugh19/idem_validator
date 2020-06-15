import validator.validator.check as check
from mock import patch
import pytest
import asyncio


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


def test_assert_block(mock_hub):
    mock_hub.OPT = {"validator": {"delimiter": ":"}}
    test_name = "a test"
    test_dict = {"assertion": "assertEqual", "expected_return": "stuff"}
    mock_hub.validator.RUNS = {test_name: {"execution_output": "stuff"}}
    mock_hub.validator.assertions.assertEqual.check.return_value = "Pass"
    result = check._assert_block(mock_hub, test_name, test_dict)
    assert result == "Pass"
    mock_hub.validator.assertions.assertEqual.check.assert_called_with(
        "stuff", "stuff", True
    )


def test_assert_block_invalid_assertion(mock_hub):
    mock_hub.OPT = {"validator": {"delimiter": ":"}}
    test_name = "a test"
    test_dict = {"assertion": "assertThing", "expected_return": "stuff"}
    mock_hub.validator.RUNS = {test_name: {"execution_output": "stuff"}}
    result = check._assert_block(mock_hub, test_name, test_dict)
    assert result == "Fail: Invalid assertion assertThing"


def test_assert_block_missing_assertion(mock_hub):
    mock_hub.OPT = {"validator": {"delimiter": ":"}}
    test_name = "a test"
    test_dict = {"expected_return": "stuff"}
    mock_hub.validator.RUNS = {test_name: {"execution_output": "stuff"}}
    result = check._assert_block(mock_hub, test_name, test_dict)
    assert (
        result
        == "Fail: Test \"a test\" missing assertion for {'expected_return': 'stuff'}"
    )


@patch("validator.validator.check._assert_block", return_value="Pass")
def test_run_assertions_multi_assertion_pass(mock_hub):
    test_name = "a test"
    mock_hub.validator.RUNS = {}
    mock_hub.validator.RUNS[test_name] = {}
    test_data = {
        "assertions": [{"assertion": "assertEqual", "expected_return": "stuff"}]
    }
    result = check._run_assertions(mock_hub, test_name, test_data)
    assert mock_hub.validator.RUNS[test_name]["assertion1"]["status"] == "Pass"
    assert mock_hub.validator.RUNS[test_name]["status"] == "Pass"


@patch("validator.validator.check._assert_block", return_value="Fail: reason")
def test_run_assertions_multi_assertion_fail(mock_hub):
    test_name = "a test"
    mock_hub.validator.RUNS = {}
    mock_hub.validator.RUNS[test_name] = {}
    test_data = {
        "assertions": [{"assertion": "assertEqual", "expected_return": "stuff"}]
    }
    result = check._run_assertions(mock_hub, test_name, test_data)
    assert mock_hub.validator.RUNS[test_name]["assertion1"]["status"] == "Fail: reason"
    assert mock_hub.validator.RUNS[test_name]["status"] == "Fail"


@patch("validator.validator.check._assert_block", return_value="Pass")
def test_run_assertions_single_assertion_pass(mock_hub):
    test_name = "a test"
    mock_hub.validator.RUNS = {}
    mock_hub.validator.RUNS[test_name] = {}
    test_data = {"assertion": "assertEqual", "expected_return": "stuff"}
    result = check._run_assertions(mock_hub, test_name, test_data)
    assert mock_hub.validator.RUNS[test_name]["status"] == "Pass"


@patch("validator.validator.check._assert_block", return_value="Fail: reason")
def test_run_assertions_single_assertion_fail(mock_hub):
    test_name = "a test"
    mock_hub.validator.RUNS = {}
    mock_hub.validator.RUNS[test_name] = {}
    test_data = {"assertion": "assertEqual", "expected_return": "stuff"}
    result = check._run_assertions(mock_hub, test_name, test_data)
    assert mock_hub.validator.RUNS[test_name]["status"] == "Fail: reason"


@pytest.mark.asyncio
@patch("validator.validator.check._run_assertions")
async def test_executor(mock_hub):
    test_name = "a test"
    test_data = {
        "module_and_function": "dummy",
        "assertion": "assertEqual",
        "expected_return": "stuff",
    }
    test = {test_name: test_data}
    mock_hub.validator.RUNS = {}
    with patch.object(mock_hub.exec, "dummy", return_value="some result") as mock_exec:
        mock_hub.validator.INQUE = asyncio.Queue()
        mock_hub.validator.INQUE.put_nowait(test)

        workers = []
        workers.append(asyncio.create_task(check.execute(mock_hub)))
        await mock_hub.validator.INQUE.join()
        for task in workers:
            task.cancel()

        mock_hub.exec.dummy.assert_called_with()
        check._run_assertions.assert_called_with(mock_hub, test_name, test_data)
        assert test_name in mock_hub.validator.RUNS
        assert isinstance(mock_hub.validator.RUNS[test_name]["duration"], float)
        assert "execution_output" not in mock_hub.validator.RUNS[test_name]


@pytest.mark.asyncio
async def test_executor_skip(mock_hub):
    test_name = "skip test"
    test_data = {"skip": True}
    test = {test_name: test_data}
    mock_hub.validator.RUNS = {}
    mock_hub.validator.INQUE = asyncio.Queue()
    mock_hub.validator.INQUE.put_nowait(test)

    workers = []
    workers.append(asyncio.create_task(check.execute(mock_hub)))
    await mock_hub.validator.INQUE.join()
    for task in workers:
        task.cancel()

    assert test_name in mock_hub.validator.RUNS
    assert isinstance(mock_hub.validator.RUNS[test_name]["duration"], float)
    assert mock_hub.validator.RUNS[test_name]["status"] == "Skip"
    assert "execution_output" not in mock_hub.validator.RUNS[test_name]
