Documentation and examples
==========================

General information
-------------------

When you launch qjobs, it reads from the config file and from command line
arguments which output do you want. Then, it gets and parses the xml output of
qstat. Some minor processings are done (such as computing the elapsed time
since submission/start time, or the number of jobs per state). The output is
then done according to the wanted format.

Output options
--------------

* ``-i, --items``

Display the list of available items and their description and exit. An *item*
is any piece of information you can get about a job (e.g. its ID or its name).

``qjobs -i`` gives::

    i: job id
    p: job priority
    n: job name
    o: job owner
    s: job state
    t: job start/submission time
    e: elapsed time since start/submission
    q: queue name without domain
    d: queue domain
    k: queue name with domain
    r: requested queue(s)
    l: number of slots used

Several options expect you feed them with a list of items. In this
documentation, if the argument descriptor for an option is ``ITEMS``,
it means you have to provide a string containing the wanted items
(``inseq`` for example).

* ``-o, --out  [ITEMS]``

Set the items used for the main output. The columns are outputted in the order
of the list. You can ask for the same item many times. By default, the width of
the columns are set according to the longest value in the job list and the
fields are left-aligned. You can set your own format with the `--out_format`
option. If no ITEMS are provided, the main output is left empty (handy if you
only need some "total" stats, e.g. the number of running jobs).

* ``-t, --total  [ITEMS]``

* ``-u, --users  [USR1,USR2,...]``

Specify the users for who you want to see the jobs. The usernames
have to be comma separated, *without* spaces. If you give an empty list, you
will get the jobs from all users.

* ``-f, --file  FILE``

Use an existing xml file (as given by ``qstat -xml``) instead of calling
``qstat``.  This option exists only for debugging purposes, you probably won't
need it in a real situation.

Formatting options
------------------

* ``--mute``

No output if there is no running or pending job. This option could be useful to
avoid useless emails if you use ``qjobs`` in a cron table.

* ``-r, --reverse``

If used, the total output is before the main output (instead of after).

* ``-s, --sort ITEMS``

Sort job list of the main output according to the given items. The sortings are
made in the order you provide the items. For exemple, if the provided list of
items is ``ips``, it means that the jobs are sorted first by ID, then by
priority and finally by state. Hence, you will get a list sorted by state, and
the jobs with same state are sorted by priority. If two jobs have the same
priority, they are sorted by ID. The sortings are made in ascending order,
except for the items specified in the ``reversed_itms`` list (``psl`` by
default) which are sorted in descending order (see Configuration options).

* ``--sep  SEP``

* ``-O, --out_format  [FMT]``

* ``--sep_tot  SEP``

* ``--width_tot  INT``

* ``--elapsed_format  FMT``

* Configuration options

The main config file (``~/.config/qjobs/qjobs.rc`` by default) contains
user-defined values for the following variables (all in the ``Defaults``
section):

================== ================================== ========================================
Variable           Default value                      Comments
================== ================================== ========================================
``out``            ``instq``                          See ``-o`` option
``total``          ``s``                              See ``-t`` option
``sort``           ``ips``                            See ``-s`` option
``reversed_itms``  ``psl``                            List of item sorted by descending order
``out_format``     None                               See ``-O`` option
``start_format``   ``{Y}-{m}-{d} {H}:{M}:{S}``        *to do*
``elapsed_format`` ``{H:03d}:{m:02d} ({D:.2f} days)`` *to do*
``width_tot``      ``120``                            See ``--width_tot`` option
``sep_tot``        ``[     ]``                        See ``--sep_tot`` option
``sep``            ``[   ]``                          See ``--sep`` option
``users``          ``$USER``                          See ``-u`` option
``editor``         ``vim``                            Editor used by ``-e`` option
``qstat_cmd``      ``qstat``                          Command launched as qstat
================== ================================== ========================================

* ``-c, --config  [FILE]``

Use ``FILE`` as config file instead of the main config file. If no file is
given, the current config (taking command line arguments into accounts) is
displayed formatted as a valid config file. This is useful to create a new
config file.

* ``--default_config``

The main config file is filled with the default value for each option.

* ``-e, --edit_config``

Open the main config file in the editor.

* ``-E, --edit_interactive``

Edit the main config file in an interactive way. For each option, the following
prompt is displayed::

    option_name: current_value (default_value)>

You can then type the new value you want and hit enter to validate.  If you
provide an empty string, the current value is kept. If you type a single ``x``,
the value is set to the default. If you want to set an actual empty string or
an actual ``x``, make sure to add one space before hitting the enter key.
