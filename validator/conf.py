CLI_CONFIG = {
    "tests": {"positional": True, "nargs": "+"},
    "render": {},
    "delimiter": {},
    "workers": {"type": int},
    "output": {"options": ["--output", "-o"],},
}
CONFIG = {
    "tests": {"default": [], "help": "The test to run when validator is called",},
    "render": {
        "default": "jinja|yaml",
        "help": "The render pipe to use, this allows for the language to be specified",
    },
    "delimiter": {"default": ":", "help": "The default assertion section delimiter",},
    "workers": {"default": "5", "help": "The number of concurrent worker processes",},
    "output": {
        "default": "nested",
        "help": "Define which outputter system should be used to display the result",
    },

}

SUBCOMMANDS = {}
DYNE = {
    "validator": ["validator"],
}
