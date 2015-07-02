# qjobs
qstat wrapper

## compatibility

qjobs only uses built-in Python modules, and should work without any problem
on both Python 2 and 3.

## installation

all you need to do is download the `qjobs` file, it is usable as-is.

## documentation/examples

to do

## TODO

This is a list of features I want to add soon.

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

config file (ConfigParser) to be able to change default (raw > file > command)
this should be done at FIRST (will make adaptation much more simpler)
-c --config to load an other config (default as ~/.config/qjobs/qjobs.rc, should create a commented example)
