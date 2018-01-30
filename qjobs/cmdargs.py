"""Parse command line arguments."""

from loam.tools import Subcmd
from . import conf
from .misc import itmfilter, rm_brackets


SUB_CMDS = {
    None: Subcmd([], {}, 'qstat wrapper for better output'),
    '': Subcmd(['general', 'jobs', 'total'], {}, ''),
    'config': Subcmd([], {}, 'configuration handling'),
    'version': Subcmd([], {}, 'print version and exit'),
}


def parse():
    """Parse arguments given in command line."""

    conf.build_parser_(SUB_CMDS)
    args, _ = conf.parse_args_()

    conf.jobs.out = itmfilter(conf.jobs.out)
    conf.total.total = itmfilter(conf.total.total, True)
    conf.jobs.sort = itmfilter(conf.jobs.sort)

    conf.jobs.sep = rm_brackets(conf.jobs.sep)
    conf.total.sep_tot = rm_brackets(conf.total.sep_tot)

    conf.jobs.start_format = conf.jobs.start_format.\
        replace('{', '%').replace('}', '')
    if not conf.jobs.out_format:
        conf.jobs.out_format = conf.jobs.sep.join(
            '{{' + itm + ':{' + itm + '}}}' for itm in conf.jobs.out)
    return args.loam_sub_name
