import pytest
import mock

@pytest.fixture(scope="function")
def hub(hub):
    for dyne in ("exec", "validator"):
        hub.pop.sub.add(dyne_name=dyne)
        if dyne in ("validator", "exec"):
            hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)

    args = [
        'testfile.tst'
    ]
    with mock.patch("sys.argv", ["validator"] + args):
        hub.pop.config.load(["validator"], "validator")

    yield hub

    # TODO Hub cleanup
    pass
