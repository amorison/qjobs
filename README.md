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
- That's it! If `~/bin` is in your PATH environment variable, you only have to
  type `qjobs` to launch the wrapper. Enjoy!

### Customization

You can customize the installation process by editing the first lines of the
script before running it.

The variable `pathScript` is the directory where the executable will be copied.
Its default value is `$HOME'/bin'`. You may want to choose a directory which is
in your path.

The variable `scriptFile` is the name of the script after installation. Its
default value is `'qjobs'`. Hence, if `pathScript` is in your path, you will
only need to type `qjobs` to launch the program.

The variable `pathConfig` is the name of the directory where the config file
will be copied. Its default value is `$HOME'/.config/qjobs'`.

The variable `configFile` is the name of the copied config file. Its default
value is `'qjobs.rc'`.

Finally, you can also force the location of the Python interpretor with the
`pythonCmd` and `pythonVersion` variables. For example, if you have a fancy
Python 2 interpretor located in `/opt/bin/myPython`, you could force its use
by setting `pythonCmd='/opt/bin/myPython'` and `pythonVersion=2`. In most
cases, you don't need to bother with these variables as the installation script
will look for a Python interpretor in your path (and adapt the script to Python
2 if needed).

Please use the `$HOME` variable instead of `~` if you change any of these
locations.  They are expanded and pasted in the installed script, which would
not be possible with the `~` symbol.

## Documentation and examples

to do

## TODO

This is a list of features I want to add soon, non sorted at all.

-g --group group by (many levels, sorted at each group level, regex name(?))

-v --verbose verbose option to display all fields

-O --format\_out with more advanced formatting
