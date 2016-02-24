"""qjobs is a qstat wrapper designed to get a better output."""

import sys
from datetime import datetime
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET

from . import cmdargs, configfile, constants
from .job import Job, JobList, JobGroup


def main():
    """execute qstat and produces output according to chosen options."""
    args = cmdargs.parse()
    if args.edit_interactive:
        print(constants.path_config+':\n')
        print('option: current value (default)> enter new value')
        print('empty string to keep current value')
        print('single x to set to default value')
        print('trailing spaces to set to an actual x/empty string', end='\n\n')
        args = vars(args)
        for opt, dflt_val in constants.default_config.items():
            new_val = input('{}: {} ({})> '.format(opt, args[opt], dflt_val))
            if new_val:
                if new_val == 'x':
                    args[opt] = dflt_val
                else:
                    args[opt] = new_val

        if not str(args['width_tot']).isdigit():
            args['width_tot'] = constants.default_config['width_tot']

        configfile.write(args, constants.path_config)
        sys.exit()

    if args.items:
        print(*('{}: {}'.format(k, v.dscr) for k, v in constants.itms.items()),
              sep='\n')
        sys.exit()

    if args.file:
        qstat_out = args.file
    else:
        qstat_out = Popen(args.qstat_cmd +
                          ' -u "' + args.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    qstat_out = ET.parse(qstat_out).getroot().iter('job_list')

    alljobs = []
    today = datetime.today()
    for j in qstat_out:
        alljobs.append(Job(j, args, today))

    if not alljobs:
        if not args.mute:
            print('No pending or running job.')
    else:
        alljobs = JobList(alljobs, args)

        out_gen = (alljobs.rep(), alljobs.rep_tot())
        for line in out_gen[args.reverse]:
            print(line)

        if args.out and args.total:
            print()

        for line in out_gen[not args.reverse]:
            print(line)


def main_wrapper():
    """Catch exception in a log file."""
    try:
        main()
    except Exception as excpt:

        from configparser import NoSectionError, MissingSectionHeaderError

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


if __name__ == '__main__':
    main_wrapper()
