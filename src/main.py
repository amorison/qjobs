#!PYTHON_CMD
"""qjobs is a qstat wrapper designed to get a better output."""

from configparser import NoSectionError, MissingSectionHeaderError
import sys

import constants


def elapsed_time(start_time, fmt):
    """return formatted elapsed time since start time"""

    from datetime import datetime

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
        for itm, itmtp in constants.itms.items():
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

        for itm in args.total.lower().replace('e', 't'):
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
        rvs = itm in constants.reversed_itms
        itm = itm.replace('e', 't')
        if itm in constants.itms:
            alljobs.sort(key=lambda job: job[itm],
                         reverse=rvs)
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
        rvs = itm.lower() in constants.reversed_itms
        tot_elaps = False
        if itm.lower() == 'e':
            tot_elaps = True
            itm = itm.replace('e', 't').replace('E', 'T')
        dct = job_counter[itm.lower()]
        if '' in dct:
            dct['not set'] = dct.pop('')

        dct = sorted(dct.items(),
                     key=lambda x: x[0],
                     reverse=rvs)
        if itm.isupper():
            dct = sorted(dct,
                         key=lambda x: x[1],
                         reverse=True)

        if tot_elaps:
            dct = list((elapsed_time(k, args.elapsed_format), v)
                       for k, v in dct)
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

    import cmdargs

    args = cmdargs.parse()
    if args.items:
        print(*('{}: {}'.format(k, v.dscr) for k, v in constants.itms.items()),
              sep='\n')
        sys.exit()

    if args.file:
        qstat_out = args.file
    else:
        qstat_out = Popen(constants.qstat_cmd +
                          ' -u "' + args.users + '" -xml -r',
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
