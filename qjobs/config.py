"""Configuration definitions."""
from os.path import expanduser
import argparse
import getpass
import pathlib
import loam.tools
from loam.tools import ConfOpt

HOME = pathlib.Path(expanduser('~'))

CONFIG_DIR = HOME / '.config' / 'qjobs'
CONFIG_FILE = CONFIG_DIR / 'config'

_ITEMS = dict(nargs='?', const='', metavar='ITEMS')
_USERS = dict(nargs='?', const='*', metavar='USR1,USR2,...')

CONF_DEF = {
    'general': {
        'qstat_cmd':
            ConfOpt('qstat', False, None, {}, True,
                    'qstat command'),
        'items':
            ConfOpt(None, True, 'i', dict(action='store_true'), False,
                    'print ITEMS list and exit'),
        'reverse':
            ConfOpt(False, True, 'r', dict(action='store_true'), False,
                    'print total before list of jobs'),
        'mute':
            ConfOpt(None, True, None, dict(action='store_true'), False,
                    'no output if no jobs'),
        'users':
            ConfOpt(getpass.getuser(), True, 'u', _USERS, True,
                    'list of printed users, leave empty to select all users'),
        'file':
            ConfOpt(None, True, 'f', dict(type=argparse.FileType('r')), False,
                    'use xmf file as input (debug purpose)'),
    },
    'jobs': {
        'out':
            ConfOpt('instq', True, 'o', _ITEMS, True,
                    'list of printed ITEMS'),
        'out_format':
            ConfOpt('', True, 'O', _ITEMS, True,
                    'format of job list output'),
        'sort':
            ConfOpt('ips', True, 's', dict(metavar='ITEMS'), True,
                    'sorting ITEMS'),
        'reversed_itms':
            ConfOpt('psl', False, None, {}, False,
                    'ITEMS sorted by descreasing value'),
        'start_format':
            ConfOpt('{Y}-{m}-{d} {H}:{M}:{S}', False, None, {}, True,
                    'e ITEM format'),
        'elapsed_format':
            ConfOpt('{H:03d}:{m:02d} ({D:.2f} days)', False, None, {}, True,
                    'e ITEM format'),
        'sep':
            ConfOpt('[   ]', True, None, {}, True,
                    'separator between columns'),
    },
    'total': {
        'total':
            ConfOpt('s', True, 't', _ITEMS, True,
                    'list of ITEMS in total section'),
        'width_tot':
            ConfOpt(120, False, None, {}, True,
                    'max output width for total section'),
        'sep_tot':
            ConfOpt('[     ]', True, None, {}, True,
                    'separator between columns'),
    },
    'config': loam.tools.config_conf_section(),
}
