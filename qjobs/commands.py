"""Commands handling."""

import sys
from datetime import datetime
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET

from loam.cli import Subcmd, CLIManager
from loam.tools import config_cmd_handler

from . import __version__, conf, constants
from .misc import itmfilter
from .job import Job, JobList


SUB_CMDS = {
    'common_': Subcmd('qstat wrapper for better output'),
    'bare_': Subcmd('', 'general', 'jobs', 'total'),
    'config': Subcmd('configuration handling'),
    'version': Subcmd('print version and exit'),
}


def parse():
    """Parse arguments given in command line."""

    climan = CLIManager(conf, **SUB_CMDS)
    args, _ = climan.parse_args()

    conf.jobs.out = itmfilter(conf.jobs.out)
    conf.total.total = itmfilter(conf.total.total, True)
    conf.jobs.sort = itmfilter(conf.jobs.sort)

    conf.jobs.start_format = conf.jobs.start_format.\
        replace('{', '%').replace('}', '')
    if not conf.jobs.out_format:
        conf.jobs.out_format = conf.jobs.sep.join(
            '{{' + itm + ':{' + itm + '}}}' for itm in conf.jobs.out)
    return args.loam_sub_name


def main(subcmd=None):
    """execute qstat and produces output according to chosen options."""
    if subcmd == 'version':
        print('qjobs version: {}'.format(__version__))
        sys.exit()

    if subcmd == 'config':
        config_cmd_handler(conf)
        sys.exit()

    if conf.general.items:
        print(*('{}: {}'.format(k, v.dscr)
                for k, v in constants.ITEMS.items()),
              sep='\n')
        sys.exit()

    if conf.general.file:
        qstat_out = conf.general.file
    else:
        qstat_out = Popen(conf.general.qstat_cmd +
                          ' -u "' + conf.general.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    qstat_out = ET.parse(qstat_out).getroot().iter('job_list')

    today = datetime.today()
    alljobs = [Job(j, today) for j in qstat_out]

    if not alljobs:
        if not conf.general.mute:
            print('No pending or running job.')
    else:
        alljobs = JobList(alljobs)

        out_gen = (alljobs.rep(), alljobs.rep_tot())
        for line in out_gen[conf.general.reverse]:
            print(line)

        if conf.jobs.out and conf.total.total:
            print()

        for line in out_gen[not conf.general.reverse]:
            print(line)
