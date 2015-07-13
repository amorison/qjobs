#!PYTHON_CMD
"""qjobs is a qstat wrapper designed to get a better output."""

import sys


def main():
    """execute qstat and produces output according to chosen options."""

    from subprocess import Popen, PIPE
    import xml.etree.ElementTree as ET

    import cmdargs
    import constants
    from misc import get_itms
    import output

    args = cmdargs.parse()
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

    alljobs, job_counter = get_itms(qstat_out, args)

    if not alljobs:
        if not args.mute:
            print('No pending or running job.')
    else:
        if args.out and not args.reverse:
            output.out(alljobs, args)
        if args.total and args.reverse:
            output.total(alljobs, job_counter, args)

        if args.out and args.total:
            print()

        if args.total and not args.reverse:
            output.total(alljobs, job_counter, args)
        if args.out and args.reverse:
            output.out(alljobs, args)


if __name__ == '__main__':

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
