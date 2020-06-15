from mock import Mock

import validator.validator.assertions.contracts.init as contract

def test_assert_return_validation_pass(mock_hub):
    ctx = Mock()
    ctx.ret = "Pass"
    result = contract.post_check(mock_hub, ctx)
    assert result == "Pass"

def test_assert_return_validation_fail(mock_hub):
    ctx = Mock()
    ctx.ret = "Fail: reason"
    result = contract.post_check(mock_hub, ctx)
    assert result == "Fail: reason"

def test_assert_return_validation_other(mock_hub):
    ctx = Mock()
    ctx.ret = "what"
    result = contract.post_check(mock_hub, ctx)
    assert result == "Fail: what"
