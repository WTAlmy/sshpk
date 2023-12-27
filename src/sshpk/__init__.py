import hashlib
import pprint
import shutil
import subprocess
import sys
from pathlib import Path

from sshpk.db import db
from sshpk.paths import (
    ID_RSA_PATH,
    ID_RSA_PUB_PATH,
    SSH_PATH,
    SSHPK_BACKUP_PATH,
    SSHPK_PATH,
)

SSHPK_MODES = ["help", "clean", "backup", "list", "copy", "delete", "load", "new"]

pp = pprint.PrettyPrinter(indent=4)


def nothing(reason: str | None, code: int = 0) -> int:
    print("No action was performed.")
    if reason:
        print("Reason: " + reason)
    return code


def clean() -> int:
    print("clean()")
    print("Removing sshpk config")
    shutil.rmtree(SSHPK_PATH)
    return 0


def read_rsa_keys() -> tuple[str | None, str | None]:
    id_rsa = None
    id_rsa_pub = None
    if ID_RSA_PATH.exists():
        with ID_RSA_PATH.open() as f:
            id_rsa = f.read()
    if ID_RSA_PUB_PATH.exists():
        with ID_RSA_PUB_PATH.open() as f:
            id_rsa_pub = f.read()
    return id_rsa, id_rsa_pub


def get_current_rsa_keys() -> tuple[str, str] | None:
    id_rsa, id_rsa_pub = read_rsa_keys()

    if id_rsa and id_rsa_pub:
        return (id_rsa, id_rsa_pub)
    if id_rsa:
        raise RuntimeError(f"Found {ID_RSA_PATH}, but not {ID_RSA_PUB_PATH}")
    if id_rsa_pub:
        raise RuntimeError(f"Found {ID_RSA_PUB_PATH}, but not {ID_RSA_PATH}")
    return None


def get_profile_paths(profile: str) -> tuple[Path, Path]:
    id_rsa_path = SSHPK_PATH / f"profile:{profile}-id-rsa"
    id_rsa_pub_path = SSHPK_PATH / f"profile:{profile}-id-rsa.pub"
    return id_rsa_path, id_rsa_pub_path


def read(path: Path) -> str:
    with path.open("r") as f:
        return f.read()


def write(path: Path, contents: str) -> None:
    with path.open("w+") as f:
        f.write(contents)


def copy(profile: str) -> int:
    print("copy()")
    keys = get_current_rsa_keys()
    if not keys:
        return nothing(f"No RSA keys found in {SSH_PATH}")

    id_rsa, id_rsa_pub = keys
    id_rsa_path, id_rsa_pub_path = get_profile_paths(profile)

    write(id_rsa_path, id_rsa)
    write(id_rsa_pub_path, id_rsa_pub)

    db["profiles"][profile] = (id_rsa_path, id_rsa_pub_path)
    return 0


def backup() -> int:
    print("backup()")
    keys = get_current_rsa_keys()
    if keys:
        digest = hashlib.md5((keys[0] + keys[1]).encode("utf-8")).hexdigest()
        shutil.copy(ID_RSA_PATH, SSHPK_BACKUP_PATH / (digest + "-id_rsa"))
        shutil.copy(ID_RSA_PUB_PATH, SSHPK_BACKUP_PATH / (digest + "-id_rsa.pub"))
    return 0


def load(profile: str) -> int:
    print("load()")
    backup()

    paths = db["profiles"][profile]
    write(ID_RSA_PATH, read(paths[0]))
    write(ID_RSA_PUB_PATH, read(paths[1]))
    return 0


def delete(profile: str) -> int:
    print("delete()")
    for path in db["profiles"][profile]:
        path.unlink()
    del db["profiles"][profile]
    return 0


def archive(profile: str) -> int:
    print("archive()")
    for path in db["profiles"][profile]:
        path.rename(str(path) + ".archive")
    del db["profiles"][profile]
    return 0


def new(profile: str) -> int:
    backup()
    cmd = ["ssh-keygen", "-q", "-t", "rsa", "-N", ""]
    subprocess.run(cmd, check=True)
    copy(profile)
    return 0


def sshpk_list() -> int:
    print("list()")
    pp.pprint(db["profiles"])
    return 0


def sshpk_help() -> int:
    print("help()")
    print(SSHPK_MODES)
    return 0


def _main() -> int:  # noqa: PLR0911
    if len(sys.argv) < 2:  # noqa: PLR2004
        sshpk_help()
        return 1

    # yeah I know
    mode = sys.argv[1]
    match mode:
        case "clean":
            return clean()
        case "help":
            return sshpk_help()
        case "copy":
            return copy(sys.argv[2])
        case "list":
            return sshpk_list()
        case "delete":
            return delete(sys.argv[2])
        case "archive":
            return archive(sys.argv[2])
        case "backup":
            return backup()
        case "load":
            return load(sys.argv[2])
        case "new":
            return new(sys.argv[2])
        case _:
            sshpk_help()
            return 1


def main() -> int:
    debug = True
    try:
        return _main()
    except Exception as e:
        print("Oh no! sshpk encountered an error.")
        if debug:
            raise e
        return 1
