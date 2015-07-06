#!PYTHON_CMD
"""qjobs is a qstat wrapper designed to get a better output."""

from configparser import ConfigParser as config_parser
from configparser import NoSectionError
from collections import OrderedDict, namedtuple

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

reversed_itms = 'psl'

default_config = {
    'out': 'instq',
    'total': 's',
    'sort': 'ips',
    'width_tot': 120,
    'sep_tot': 5,
    'sep': 3,
    'users': 'USER_NAME'}


def parse_args():
    """parse arguments given in command line and fetch
    default config from config file."""

    import argparse
    parser = argparse.ArgumentParser(
        description='qstat wrapper for better output. \
            Available ITEMS are "' + ''.join(itms.keys()) +
        '" see -i option for their description.', add_help=False)
    parser.add_argument('-c', '--config',
                        default='PATH_CONFIG',
                        metavar='FILE',
                        help='specify config file')

    args, remaining_argv = parser.parse_known_args()
    try:
        conf_parser = config_parser()
        conf_parser.read(args.config)
        defaults = dict(conf_parser.items('Defaults'))
    except NoSectionError:
        print('Cannot read config file, run install.sh script')
        defaults = default_config

    parser = argparse.ArgumentParser(parents=[parser])
    parser.add_argument('-i', '--items', action='store_true',
                        help='display descriptions of items and exit')
    parser.add_argument('-o', '--out', nargs='?', const='', metavar='ITEMS',
                        help='specify which items are displayed.')
    parser.add_argument('-t', '--total', nargs='?', const='', metavar='ITEMS',
                        help='specify items for which you want \
                                to count the jobs.')
    parser.add_argument('-s', '--sort', metavar='ITEMS',
                        help='specify the items to use to sort the jobs')
    parser.add_argument('-u', '--users', nargs='?', const='*',
                        metavar='USR1,USR2,...',
                        help='specify list of users, use commas \
                            to separate usernames, empty list \
                            will list jobs of all users')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'),
                        help='use given xml file as input (for debug)')
    parser.add_argument('--sep', type=int, metavar='INT',
                        help='number of spaces between `out` columns')
    parser.add_argument('--width_tot', type=int, metavar='INT',
                        help='max width for `total` columns')
    parser.add_argument('--sep_tot', type=int, metavar='INT',
                        help='number of spaces between `total` columns')

    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)

    columns = ''
    for itm in args.out:
        if itm in itms:
            columns += itm
    args.out = columns

    totals = ''
    for itm in args.total:
        if itm.lower() in itms:
            totals += itm
    args.total = totals

    return args


def get_itms(qstat_out, totals):
    """extract data from xml job tree
    and count totals"""

    from datetime import datetime, timedelta
    import xml.etree.ElementTree as ET

    jobs_list = ET.parse(qstat_out).getroot().iter('job_list')

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
            delta = datetime.today() -\
                datetime.strptime(job['t'], '%Y-%m-%d %H:%M:%S')
            job['e'] = str(timedelta(days=delta.days, seconds=delta.seconds,
                                     microseconds=0))
        else:
            job['t'] = 'not set'
            job['e'] = 'not set'

        for itm in totals.lower():
            if itm not in job_counter:
                job_counter[itm] = {}
            if job[itm] in job_counter[itm]:
                job_counter[itm][job[itm]] += 1
            else:
                job_counter[itm][job[itm]] = 1

        alljobs.append(job)

    return alljobs, job_counter


def print_jobs(alljobs, job_counter, args):
    """produces ouput according to chosen options."""

    from itertools import zip_longest as ziplgst
    from math import ceil

    if args.out:
        for itm in args.sort:
            if itm in itms:
                alljobs.sort(key=lambda job: job[itm],
                             reverse=(itm in reversed_itms))
        mlitm = {}
        for itm in args.out:
            mlitm[itm] = max(len(job[itm]) for job in alljobs)

        for job in alljobs:
            print(*(job[itm].ljust(mlitm[itm]) for itm in args.out),
                  sep=' '*args.sep)
        if args.total:
            print()

    if args.total:
        print('tot: {}'.format(len(alljobs)))
        for itm in args.total:
            order_by_keys = 0
            if itm.isupper():
                order_by_keys = 1
                itm = itm.lower()
            dct = job_counter[itm]
            if '' in dct:
                dct['not set'] = dct.pop('')
            dct = sorted(dct.items(),
                         key=lambda x: x[order_by_keys],
                         reverse=(itm in reversed_itms) or order_by_keys)
            mlk = max(len(k) for k, _ in dct)
            mlv = max(len(str(v)) for _, v in dct)
            spr = ' '*args.sep_tot
            nfld = (args.width_tot+len(spr))//(mlk+mlv+2+len(spr))
            if nfld == 0:
                nfld = 1

            dct = ziplgst(*(iter(dct), ) * int(ceil(len(dct)/float(nfld))),
                          fillvalue=(None, None))
            dct = zip(*dct)

            print()
            for line in dct:
                print(*('{}: {}'.format(k.ljust(mlk), str(v).rjust(mlv))
                        for k, v in line if (k, v) != (None, None)),
                      sep=spr)


def main():
    """execute qstat and produces output according to chosen options."""

    from subprocess import Popen, PIPE
    import sys

    args = parse_args()
    if args.items:
        print(*('{}: {}'.format(k, v.dscr) for k, v in itms.items()),
              sep='\n')
        sys.exit()

    if args.file:
        qstat_out = args.file
    else:
        qstat_out = Popen('QSTAT_CMD -u "' + args.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    alljobs, job_counter = get_itms(qstat_out, args.total)

    if not alljobs:
        print('No pending or running job.')
    else:
        print_jobs(alljobs, job_counter, args)


if __name__ == '__main__':
    main()
