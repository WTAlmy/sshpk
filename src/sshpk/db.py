import atexit
import shelve
import time
from pathlib import Path

from sshpk.paths import SSH_PATH, SSHPK_BACKUP_PATH, SSHPK_CONFIG_PATH, SSHPK_PATH

if not SSH_PATH.exists():
    raise RuntimeError(f"Missing {SSH_PATH}")

if not SSHPK_PATH.exists():
    Path.mkdir(SSHPK_PATH)

if not SSHPK_BACKUP_PATH.exists():
    Path.mkdir(SSHPK_BACKUP_PATH)

db = shelve.open(str(SSHPK_CONFIG_PATH), writeback=True)

if not db.get("initialized", None):
    db["initialized"] = time.time()
    db["profiles"] = {}


@atexit.register
def close_db() -> None:
    db.close()
