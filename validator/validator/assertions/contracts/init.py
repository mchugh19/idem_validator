def sig_check(hub, output, expected, print_result: bool):
    pass


def post_check(hub, ctx):
    result_prefix = ("Pass", "Fail")
    ret = ctx.ret
    if not ret.startswith(result_prefix):
        assertion_name = ".".join(ctx.func.__module__.split(".")[-2:])
        hub.log.error(
            f"Problem with assertion output for {assertion_name}. Return does not begin with 'Pass' or 'Fail', rewriting to failure"
        )
        ret = f"Fail: {ret}"
    return ret
