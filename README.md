# qjobs

qstat wrapper

## Compatibility

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor modifications are required for
this script to work with Python 2. If needed, these modifications are
automatically made by the `install.sh` script.

## Installation

The installation is made as simple as possible for you. Everything is managed
by the installation script `install.sh`.

- Allow execution of `install.sh` with the command `chmod u+x install.sh`.
- Run the installation script with `./install.sh`.
- If the script doesn't manage to find qstat and/or Python in your PATH, you
  will be asked to enter their location.
- You will have to choose an editor (used with the `-e` option of qjobs to edit
  the config file), leave an empty line to use vim.
- That's it! If `~/bin` is in your PATH environment variable, you only have to
  type `qjobs` to launch the wrapper. Enjoy!

If you want to uninstall `qjobs`, call the installation script with the `-u`
option: `./install.sh -u`.

To customize the installation process, please see [the related wiki
page](https://github.com/amorison/qjobs/wiki/Installation).

## Documentation and examples

The complete documentation will be in the wiki (to do).
