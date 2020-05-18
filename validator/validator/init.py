def __init__(hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name='output')
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.load_subdirs(hub.exec, recurse=True)


def cli(hub):
    hub.pop.config.load(["validator"], cli="validator")
    hub.pop.loop.start(hub.validator.check.run_test())
