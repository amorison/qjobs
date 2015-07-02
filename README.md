# qjobs

qstat wrapper

## compatibility

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor
modifications are required for this script to work with
Python 2.
You have to:
- adapt the she-bang;
- add `from future import print_function` at the very beginning
of the script;
- rename the `configparser` module to `ConfigParser`;
- rename the `ConfigParser()` function to `SafeConfigParser()`.

## installation

Put `qjobs` in a directory of your choice (you might want to put it in
a directory which is in your PATH environment variable).

Put `qjobs.rc` (config file) in `~/.config/qjobs/qjobs.rc`

That's it!

## documentation/examples

to do

## TODO

This is a list of features I want to add soon.

an installation script

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
