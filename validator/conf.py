CLI_CONFIG = {
    "tests": {
        "positional": True,
        "nargs": "+"
    }
}
CONFIG = {
    "tests": {"default": [], "help": "The test to run when validator is called",},
}

SUBCOMMANDS = {}
DYNE = {
    "validator": ["validator"],
}
