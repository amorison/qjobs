#!PYTHON_CMD
"""qjobs is a qstat wrapper designed to get a better output."""

from configparser import ConfigParser as config_parser
from configparser import NoSectionError

items = 'ipnosteqdkrl'
items_description = [
    ('i', 'job id'),
    ('p', 'job priority'),
    ('n', 'job name'),
    ('o', 'job owner'),
    ('s', 'job state'),
    ('t', 'job start/submission time'),
    ('e', 'elapsed time since start/submission'),
    ('q', 'queue name without domain'),
    ('d', 'queue domain'),
    ('k', 'queue name with domain'),
    ('r', 'requested queue(s)'),
    ('l', 'number of slots used')]
default_config = {
    'out': 'instq',
    'total': 's',
    'sort': 'ips',
    'width_tot': 120,
    'sep_tot': 5,
    'sep': 3,
    'users': 'USER_NAME'}
reversed_items = 'psl'


def parse_args():
    """parse arguments given in command line and fetch
    default config from config file."""

    import argparse
    parser = argparse.ArgumentParser(
        description='qstat wrapper for better output. \
            Available ITEMS are "' + items +
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
    return args


def main():
    """execute qstat and produces output according to chosen options."""

    from datetime import datetime, timedelta
    from itertools import zip_longest as ziplgst
    from math import ceil
    from subprocess import Popen, PIPE
    import sys
    import xml.etree.ElementTree as ET

    args = parse_args()
    if args.items:
        print(*('{}: {}'.format(k, v) for k, v in items_description),
              sep='\n')
        sys.exit()

    if args.file:
        qstat_out = args.file
    else:
        qstat_out = Popen('command qstat -u "' + args.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    columns = ''
    for itm in args.out:
        if itm in items:
            columns += itm

    totals = ''
    for itm in args.total:
        if itm.lower() in items:
            totals += itm

    jobs_list = ET.parse(qstat_out).getroot().iter('job_list')

    alljobs = []
    job_counter = {}

    for j in jobs_list:
        job = {}
        job['i'] = j.find('JB_job_number').text
        job['p'] = j.find('JAT_prio').text
        job['n'] = j.find('JB_name').text
        job['o'] = j.find('JB_owner').text
        job['s'] = j.find('state').text
        job['q'] = ''
        job['d'] = ''
        job['k'] = ''
        job['l'] = j.find('slots').text
        if job['s'] == 'r':
            job['t'] = j.find('JAT_start_time').text
            job['k'] = j.find('queue_name').text
            job['q'], job['d'] = job['k'].rsplit('@')
        elif job['s'] in ['dt', 'dr']:
            job['t'] = j.find('JAT_start_time').text
        else:
            try:
                job['t'] = j.find('JB_submission_time').text
            except AttributeError:
                job['t'] = None
        if job['t']:
            job['t'] = job['t'].replace('T', ' ')
            start_time = datetime.strptime(job['t'], '%Y-%m-%d %H:%M:%S')
            delta = datetime.today() - start_time
            job['e'] = str(timedelta(days=delta.days, seconds=delta.seconds,
                                     microseconds=0))
        else:
            job['t'] = 'not set'
            job['e'] = 'not set'
        req_list = j.iter('hard_req_queue')
        job['r'] = ', '.join(sorted(req.text for req in req_list))

        for itm in totals.lower():
            if itm not in job_counter:
                job_counter[itm] = {}
            if job[itm] in job_counter[itm]:
                job_counter[itm][job[itm]] += 1
            else:
                job_counter[itm][job[itm]] = 1

        alljobs.append(job)

    if not alljobs:
        print('No pending or running job.')
    else:
        if columns:
            for itm in args.sort:
                if itm in items:
                    alljobs.sort(key=lambda job: job[itm],
                                 reverse=(itm in reversed_items))
            mlitm = {}
            for itm in columns:
                mlitm[itm] = max(len(job[itm]) for job in alljobs)

            for job in alljobs:
                print(*(job[itm].ljust(mlitm[itm]) for itm in columns),
                      sep=' '*args.sep)
            if totals:
                print()

        if totals:
            print('tot: {}'.format(len(alljobs)))
            for itm in totals:
                order_by_keys = 0
                if itm.isupper():
                    order_by_keys = 1
                    itm = itm.lower()
                dct = job_counter[itm]
                if '' in dct:
                    dct['not set'] = dct.pop('')
                dct = sorted(dct.items(),
                             key=lambda x: x[order_by_keys],
                             reverse=(itm in reversed_items) or order_by_keys)
                mlk = max(len(k) for k, _ in dct)
                mlv = max(len(str(v)) for _, v in dct)
                spr = ' '*args.sep_tot
                wdt = args.width_tot
                nfld = (wdt+len(spr))//(mlk+mlv+2+len(spr))
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

if __name__ == '__main__':
    main()
