#!PYTHON_CMD
"""qjobs is a qstat wrapper designed to get a better output."""

from configparser import ConfigParser as config_parser
from configparser import NoSectionError, MissingSectionHeaderError
from collections import OrderedDict, namedtuple
import sys

Itmtp = namedtuple('Itmtp', ['dscr', 'xml_tag'])

itms = OrderedDict((
    ('i', Itmtp('job id', ['JB_job_number'])),
    ('p', Itmtp('job priority', ['JAT_prio'])),
    ('n', Itmtp('job name', ['JB_name'])),
    ('o', Itmtp('job owner', ['JB_owner'])),
    ('s', Itmtp('job state', ['state'])),
    ('t', Itmtp('job start/submission time', ['JAT_start_time',
                                              'JB_submission_time'])),
    ('e', Itmtp('elapsed time since start/submission', [])),
    ('q', Itmtp('queue name without domain', [])),
    ('d', Itmtp('queue domain', [])),
    ('k', Itmtp('queue name with domain', ['queue_name'])),
    ('r', Itmtp('requested queue(s)', ['hard_req_queue'])),
    ('l', Itmtp('number of slots used', ['slots']))
    ))

reversed_itms = 'psel'

qstat_cmd = 'QSTAT_CMD'

path_config = 'PATH_CONFIG'

dflt_section = 'Defaults'

default_config = OrderedDict((
    ('out', 'instq'),
    ('total', 's'),
    ('sort', 'ips'),
    ('elapsed_format', '{H:03d}:{m:02d} ({D:.2f} days)'),
    ('width_tot', 120),
    ('sep_tot', '[     ]'),
    ('sep', '[   ]'),
    ('users', 'USER_NAME')
    ))


def read_config(args):
    """read config file"""

    config_file = args.config
    if not config_file:
        config_file = path_config

    try:
        conf_parser = config_parser()
        conf_parser.read(config_file)
        defaults = OrderedDict(conf_parser.items(dflt_section))
    except (NoSectionError, MissingSectionHeaderError):
        if args.config:
            print('Cannot read config file! Run install script.')
        defaults = OrderedDict()

    for opt, val in default_config.items():
        if opt not in defaults:
            defaults[opt] = val

    if not str(defaults['width_tot']).isdigit():
        defaults['width_tot'] = default_config['width_tot']

    return defaults


def write_config(args, out_stream):
    """write config file"""

    config = config_parser()
    config.add_section(dflt_section)
    for opt in default_config:
        config.set(dflt_section, opt, str(args[opt]).strip())

    if out_stream is sys.stdout:
        config.write(out_stream)
    else:
        with open(out_stream, 'w') as out_file:
            config.write(out_file)


def rm_brackets(string):
    """remove [ ] if at 1st and last char"""

    if string[0] == '[':
        string = string[1:]
    if string[-1] == ']':
        string = string[:-1]

    return string


def parse_args():
    """parse arguments given in command line and fetch
    default config from config file."""

    import argparse

    parser = argparse.ArgumentParser(
        description='qstat wrapper for better output. \
            Available ITEMS are "' + ''.join(itms.keys()) +
        '" see -i option for their description.', add_help=False)
    parser.add_argument('-c', '--config',
                        nargs='?',
                        const=None,
                        default=path_config,
                        metavar='FILE',
                        help='specify config file, write current config \
                              if called without argument')
    parser.add_argument('--default_config', action='store_true',
                        help='config file set to default config')

    args, remaining_argv = parser.parse_known_args()

    if args.default_config:
        write_config(default_config, path_config)
        sys.exit()

    config_to_stdout = not args.config
    defaults = read_config(args)

    parser = argparse.ArgumentParser(parents=[parser])
    parser.add_argument('-i', '--items', action='store_true',
                        help='display descriptions of items and exit')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='total before out')
    parser.add_argument('-o', '--out', nargs='?', const='', metavar='ITEMS',
                        help='specify which items are displayed.')
    parser.add_argument('-t', '--total', nargs='?', const='', metavar='ITEMS',
                        help='specify items for which you want \
                                to count the jobs.')
    parser.add_argument('-s', '--sort', metavar='ITEMS',
                        help='specify the items to use to sort the jobs')
    parser.add_argument('--elapsed_format', metavar='FMT',
                        help='specify e item format')
    parser.add_argument('-u', '--users', nargs='?', const='*',
                        metavar='USR1,USR2,...',
                        help='specify list of users, use commas \
                            to separate usernames, empty list \
                            will list jobs of all users')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'),
                        help='use given xml file as input (for debug)')
    parser.add_argument('--sep',
                        help='separator between `out` columns')
    parser.add_argument('--width_tot', type=int, metavar='INT',
                        help='max width for `total` columns')
    parser.add_argument('--sep_tot',
                        help='separator between `total` columns')
    parser.add_argument('--mute', action='store_true',
                        help='no output if no jobs')
    parser.add_argument('-e', '--edit_config', action='store_true',
                        help='edit config file')

    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)

    args.out = ''.join((itm for itm in args.out
                        if itm in itms))
    args.total = ''.join((itm for itm in args.total
                          if itm.lower() in itms))

    if config_to_stdout:
        write_config(vars(args), sys.stdout)
        sys.exit()

    if args.edit_config:
        print(path_config+':\n')
        print('option: current value (default)> enter new value')
        print('empty string to keep current value')
        print('single x to set to default value')
        print('trailing spaces to set to an actual x/empty string', end='\n\n')
        args = vars(args)
        for opt, dflt_val in default_config.items():
            new_val = input('{}: {} ({})> '.format(opt, args[opt], dflt_val))
            if new_val:
                if new_val == 'x':
                    args[opt] = dflt_val
                else:
                    args[opt] = new_val

        if not str(args['width_tot']).isdigit():
            args['width_tot'] = default_config['width_tot']

        write_config(args, path_config)
        sys.exit()

    args.sep = rm_brackets(args.sep)
    args.sep_tot = rm_brackets(args.sep_tot)

    return args


def elapsed_time(start_time, fmt):
    """return formatted elapsed time since start time"""

    from datetime import datetime, timedelta

    delta = datetime.today() - \
            datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    dct = {}
    dct['d'] = delta.days
    dct['h'], rmd = divmod(delta.seconds, 3600)
    dct['m'], dct['s'] = divmod(rmd, 60)
    dct['S'] = 86400 * delta.days + delta.seconds
    dct['M'] = dct['S'] // 60
    dct['H'] = dct['S'] // 3600
    dct['D'] = dct['S'] / 86400.

    return fmt.format(**dct)


def get_itms(jobs_list, args):
    """extract data from xml job tree
    and count totals"""

    alljobs = []
    job_counter = {}

    for j in jobs_list:
        job = {}
        for itm, itmtp in itms.items():
            job[itm] = ''
            for tag in itmtp.xml_tag:
                elts = j.iter(tag)
                job[itm] = ', '.join(sorted(elt.text for elt in elts
                                            if elt.text))
                if job[itm]:
                    break

        if job['k']:
            job['q'], job['d'] = job['k'].rsplit('@')

        if job['t']:
            job['t'] = job['t'].replace('T', ' ')
            job['e'] = elapsed_time(job['t'], args.elapsed_format)
        else:
            job['t'] = 'not set'
            job['e'] = 'not set'

        for itm in args.total.lower():
            if itm not in job_counter:
                job_counter[itm] = {}
            if job[itm] in job_counter[itm]:
                job_counter[itm][job[itm]] += 1
            else:
                job_counter[itm][job[itm]] = 1

        alljobs.append(job)

    return alljobs, job_counter


def print_out(alljobs, args):
    """produces output of jobs list"""

    for itm in args.sort:
        if itm in itms:
            alljobs.sort(key=lambda job: job[itm if itm != 'e' else 't'],
                         reverse=(itm in reversed_itms))
    mlitm = {}
    for itm in args.out:
        mlitm[itm] = max(len(job[itm]) for job in alljobs)

    for job in alljobs:
        print(*(job[itm].ljust(mlitm[itm]) for itm in args.out),
              sep=args.sep)


def print_total(alljobs, job_counter, args):
    """produces output of totals"""

    from itertools import zip_longest as ziplgst
    from math import ceil

    print('tot: {}'.format(len(alljobs)))
    for itm in args.total:
        dct = job_counter[itm.lower()]
        if '' in dct:
            dct['not set'] = dct.pop('')

        dct = sorted(dct.items(),
                     key=lambda x: x[0],
                     reverse=itm.lower() in reversed_itms)
        if itm.isupper():
            dct = sorted(dct,
                         key=lambda x: x[1],
                         reverse=True)

        mlk = max(len(k) for k, _ in dct)
        mlv = max(len(str(v)) for _, v in dct)
        nfld = (args.width_tot+len(args.sep_tot)) // \
               (mlk+mlv+2+len(args.sep_tot))
        if nfld == 0:
            nfld = 1

        dct = ziplgst(*(iter(dct), ) * int(ceil(len(dct)/float(nfld))),
                      fillvalue=(None, None))
        dct = zip(*dct)

        print()
        for line in dct:
            print(*('{}: {}'.format(k.ljust(mlk), str(v).rjust(mlv))
                    for k, v in line if (k, v) != (None, None)),
                  sep=args.sep_tot)


def main():
    """execute qstat and produces output according to chosen options."""

    from subprocess import Popen, PIPE
    import xml.etree.ElementTree as ET

    args = parse_args()
    if args.items:
        print(*('{}: {}'.format(k, v.dscr) for k, v in itms.items()),
              sep='\n')
        sys.exit()

    if args.file:
        qstat_out = args.file
    else:
        qstat_out = Popen(qstat_cmd + ' -u "' + args.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    qstat_out = ET.parse(qstat_out).getroot().iter('job_list')

    alljobs, job_counter = get_itms(qstat_out, args)

    if not alljobs:
        if not args.mute:
            print('No pending or running job.')
    else:
        if args.out and not args.reverse:
            print_out(alljobs, args)
        if args.total and args.reverse:
            print_total(alljobs, job_counter, args)

        if args.out and args.total:
            print()

        if args.total and not args.reverse:
            print_total(alljobs, job_counter, args)
        if args.out and args.reverse:
            print_out(alljobs, args)


if __name__ == '__main__':
    try:
        main()
    except Exception as excpt:
        if excpt not in (SystemExit, NoSectionError,
                         MissingSectionHeaderError):
            import logging
            from tempfile import NamedTemporaryFile

            tmpf = NamedTemporaryFile(prefix='qjobs', suffix='.log',
                                      delete=False)
            tmpf.close()
            logging.basicConfig(filename=tmpf.name, level=logging.DEBUG)
            logging.exception('qjobs exception log:')
            print('ERROR! Please check', tmpf.name, 'for more information.')
            sys.exit()
        raise
