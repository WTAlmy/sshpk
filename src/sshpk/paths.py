from pathlib import Path

SSH_PATH = Path.home() / ".ssh"
ID_RSA_PATH = SSH_PATH / "id_rsa"
ID_RSA_PUB_PATH = SSH_PATH / "id_rsa.pub"

SSHPK_PATH = SSH_PATH / "sshpk"
SSHPK_CONFIG_PATH = SSHPK_PATH / "sshpk"
SSHPK_BACKUP_PATH = SSHPK_PATH / "backups"
