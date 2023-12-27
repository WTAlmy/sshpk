## SSH PK

### SSH Profile Kit

I spent a few hours writing this to save me a few minutes over my lifetime

#### Description

Allows you to swap `id_rsa` and `id_rsa.pub` pairs on the fly. Mainly useful if you are using multiple GitHub accounts.

#### Setup

From top level directory (containing this README):
`pip3 install .`

#### Develop

`cd src && python3 -m sshpk`

#### Usage

```bash
# List of commands
$ sshpk help
> ['help', 'clean', 'backup', 'list', 'copy', 'delete', 'load', 'new']

# Copy existing key pairs to a new profile
$ sshpk copy my_fav_existing_keys

# Generate a new key pair, profile foo, and switch to it
$ sshpk new foo

# Generate another key pair, profile bar, and switch to it
$ sshpk new bar

# List profiles
$ sshpk list
> foo
> bar

# Load profile foo
$ sshpk load foo

# Delete profile bar
$ sshpk delete bar

# Reset to initial state
$ sshpk load my_fav_existing_keys
$ sshpk clean
```

#### Recovery

Something fucked up? Look in `~/.ssh/sshpk/backups` for your keys.
