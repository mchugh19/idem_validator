def __init__(hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.load_subdirs(hub.validator, recurse=True)
    hub.validator.RUNS = {}


def cli(hub):
    hub.pop.config.load(["validator"], cli="validator")
    hub.pop.loop.start(hub.validator.check.main())
