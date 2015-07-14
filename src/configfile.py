"""provides read/write config file functions"""

from configparser import ConfigParser as config_parser

import constants


def read(args):
    """read config file"""

    from configparser import NoSectionError, MissingSectionHeaderError

    config_file = args.config
    if not config_file:
        config_file = constants.path_config

    try:
        conf_parser = config_parser(interpolation=None)
        conf_parser.read(config_file)
        defaults = constants.OrderedDict(
            conf_parser.items(constants.dflt_section))
    except (NoSectionError, MissingSectionHeaderError):
        if args.config:
            print('Cannot read config file! Run install script.')
        defaults = constants.OrderedDict()

    for opt, val in constants.default_config.items():
        if opt not in defaults:
            defaults[opt] = val

    if not str(defaults['width_tot']).isdigit():
        defaults['width_tot'] = constants.default_config['width_tot']

    return defaults


def write(args, out_stream):
    """write config file"""

    import sys

    config = config_parser(interpolation=None)
    config.add_section(constants.dflt_section)
    for opt in constants.default_config:
        config.set(constants.dflt_section, opt, str(args[opt]).strip())

    if out_stream is sys.stdout:
        config.write(out_stream)
    else:
        with open(out_stream, 'w') as out_file:
            config.write(out_file)
