"""qjobs is a qstat wrapper designed to get a better output."""

import sys
from datetime import datetime
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET
from loam.tools import config_cmd_handler
from . import conf, cmdargs, constants
from .job import Job, JobList, JobGroup


def main(subcmd=None):
    """execute qstat and produces output according to chosen options."""
    if subcmd == 'config':
        config_cmd_handler(conf)
        sys.exit()

    if conf.general.items:
        print(*('{}: {}'.format(k, v.dscr) for k, v in constants.itms.items()),
              sep='\n')
        sys.exit()

    if conf.general.file:
        qstat_out = conf.general.file
    else:
        qstat_out = Popen(conf.general.qstat_cmd +
                          ' -u "' + conf.general.users + '" -xml -r',
                          shell=True, stdout=PIPE).stdout

    qstat_out = ET.parse(qstat_out).getroot().iter('job_list')

    alljobs = []
    today = datetime.today()
    for j in qstat_out:
        alljobs.append(Job(j, today))

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
