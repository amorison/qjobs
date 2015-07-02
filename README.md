# qjobs

qstat wrapper

## compatibility

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor
modifications are required for this script to work with
Python 2.
You have to:
- adapt the she-bang;
- add `from __future__ import print_function` at the very beginning
of the script;
- rename the `configparser` module to `ConfigParser`;
- rename the `ConfigParser()` function to `SafeConfigParser()`.

## installation

Allow execution of `install.sh` with the command `chmod +x install.sh`.

If needed, edit the script to change the directory where the script and/or the
config file are copied. By default, the script `qjobs` is copied in `~/bin`
(variable `pathScript`). The config file is copied in `~/.config/qjobs` (variable
`pathConfig`) and if named `qjobs.rc` (variable `configFile`).
Please use the `$HOME` variable instead of `~` if you change these locations.

Run the installation script with `./install.sh`.

That's it! If `~/bin` (or the location you choose) is in the PATH environment
variable, you only have to type `qjobs` to launch the wrapper.

## documentation/examples

to do

## TODO

This is a list of features I want to add soon, non sorted at all.

--sep (-p) to change separator (with '   ' default value)

-s --sort sort by sort with key lambda x: x[args.sort], have to be in iunostql (which should be a constant)...

-g --group group by (many levels, sorted at each group level, regex name(?))
(these two (only g btw) should depend on whether -d is active or not < already OK)

-t --total totals (-o should accept empty string (nargs='\*'), or need a commutator, like -m, to mute)

-v --verbose verbose option to display all fields

-O --format\_out with more advanced formatting

-u --user user1,user2
r requested queues
d time difference (datetime module)
