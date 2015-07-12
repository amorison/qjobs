# qjobs

qstat wrapper

## Compatibility

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor modifications are required for
this script to work with Python 2. If needed, these modifications are
automatically made by the `install.sh` script.

## Installation

### Quick installation

- Allow execution of `install.sh` with the command `chmod u+x install.sh`.
- Run the installation script with `./install.sh`.
- If the script doesn't manage to find qstat and/or Python in your PATH, you
  will be asked to enter their location.
- That's it! If `~/bin` is in your PATH environment variable, you only have to
  type `qjobs` to launch the wrapper. Enjoy!

If you want to uninstall `qjobs`, call the installation script with the `-u`
option: `./install.sh -u`.

### Customization

_(will be moved to the wiki)_

By default, the installation script does the following:

- create a `qjobs` directory in `~/.local/share` where the Python modules are
  copied;
- create a `qjobs` directory in `~/.config` where the default config file is
  put;
- create a symbolic link named `qjobs` in `~/bin` which points toward the main
  module in `~/.local/share`.

You can customize the installation process by editing the first lines of the
script before running it.

Please use the `$HOME` variable instead of `~` if you change any of these
locations.  They are expanded and pasted in the installed script, which would
not be possible with the `~` symbol.

The variable `pathScript` is the directory where the link to the main module
will be created.  Its default value is `$HOME'/bin'`. You may want to choose a
directory which is in your path.

The variable `scriptFile` is the name of the said link. Its default value is
`'qjobs'`. Hence, if `pathScript` is in your path, you will only need to type
`qjobs` to launch the program.

The variable `installDir` is the name of the directory where the Python modules
will be copied. Its default value is `$HOME'/.local/share'`.

The variable `configDir` is the name of the directory where the config file
will be copied. Its default value is `$HOME'/.config'`.

You can force the location of the `qstat` program with the `qstatCmd` variable.

You can set the editor which will be used to edit the config file with the `-e`
option with the `editor` variable. The default editor is `vim`.

Finally, you can also force the location of the Python interpretor with the
`pythonCmd` and `pythonVersion` variables. For example, if you have a fancy
Python 2 interpretor located in `/opt/bin/myPython`, you could force its use
by setting `pythonCmd='/opt/bin/myPython'` and `pythonVersion=2`. In most
cases, you don't need to bother with these variables as the installation script
will look for a Python interpretor in your path (and adapt the script to Python
2 if needed).

## Documentation and examples

The complete documentation will be in the wiki (to do).
