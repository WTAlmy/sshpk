# SSH PK

## SSH Profile Kit

I spent a few hours writing this to save me a few minutes over my lifetime

### Description

Allows you to swap `id_rsa` and `id_rsa.pub` pairs on the fly. Mainly useful if you are using multiple GitHub accounts.

### Usage

`sshpk help`

#### Copy existing `id_rsa` and `id_rsa.pub`

`sshpk copy my_fav_existing_keys`

#### Generate a new `id_rsa` and `id_rsa.pub`

`sshpk new foo`

#### Generate another `id_rsa` and `id_rsa.pub`

`sshpk new bar`

#### List profiles

`sshpk list`

#### Swap from `bar` to `foo`

`sshpk load foo`

#### Get rid of `bar`

`sshpk delete bar`

#### Reset to prior state

`sshpk load my_fav_existing_keys`
`sshpk clean`

### Recovery

Something fucked up? Look in `~/.ssh/sshpk/backups` for your keys.
