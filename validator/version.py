# -*- coding: utf-8 -*-
def get_ver():
    """
    Gather the version number from git
    """
    import subprocess

    proc = subprocess.Popen(["git", "describe"], stdout=subprocess.PIPE)
    if proc.wait():
        return
    v = proc.stdout.read().decode().strip()
    if "-" not in v:
        ret = v
    else:
        csum = v[v.rindex("-") + 1 :]
        base = v[: v.rindex("-")]
        count = base[base.rindex("-") + 1 :]
        tag = base[: base.rindex("-")]
        ret = f"{tag}.post{count}+{csum}"
    return ret


version = get_ver()
