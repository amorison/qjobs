Welcome to the qjobs documentation!
===================================

qjobs is an attempt to get a cleaner and more customizable output than the one
provided by qstat (Sun Grid Engine).

For example, when I make a parameter space exploration, I usually have quite
long job's names (though reduced to the substantial minimum) to be able to know
exactly which cases are still running and which cases are ready for
post-processing. The fact qstat cuts the job's names ruins all the efforts made
to have clear and useful names.

That's why I created qjobs. The default output looks like this::

    5599091   s-2.56e6-1.e0    r    2015-06-25 10:03:40   queue1
    5599092   s-2.56e6-3.e1    r    2015-06-25 10:03:40   queue36
    5599093   s-2.56e6-1.e2    r    2015-06-25 10:03:40   queue4
    5599094   s-2.56e6-3.e2    r    2015-06-25 10:03:40   queue42
    5599095   s-2.56e6-1.e3    r    2015-06-25 10:03:40   queue36
    5599096   s-2.56e6-3.e4    qw   2015-06-25 10:02:40
    5599097   s-2.56e6-1.e5    qw   2015-06-25 10:02:40
    5599098   s-5.12e6-1.e-3   qw   2015-06-25 10:02:40
    5599099   s-5.12e6-3.e-2   qw   2015-06-25 10:02:40
    
    tot: 9
    
    r : 5     qw: 4

The job names (2nd column) are not cut, the priority and owner columns are
removed and the domain of the queue is not displayed. As a nice bonus, the
total number of job as well as the number of jobs per state are displayed at
the end.

Of course, this formatting is completely customizable, with a config
file or temporarily via command line options. If you prefer, you can cut the
job name, display the domain of the queue, count the jobs grouped by the number
of elapsed days since start/submission, etc.

For a complete list of options, see :doc:`commands`.
