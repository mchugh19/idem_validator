CLI_CONFIG = {
    "tests": {
        "positional": True,
        "nargs": "+"
    },
    "render": {},
    "delimiter": {}
}
CONFIG = {
    "tests": {"default": [], "help": "The test to run when validator is called",},
    "render": {
        "default": "jinja|yaml",
        "help": "The render pipe to use, this allows for the language to be specified",
    },
    "delimiter": {
        "default": ":",
        "help": "The default assertion section delimiter",
    }
}

SUBCOMMANDS = {}
DYNE = {
    "validator": ["validator"],
}
