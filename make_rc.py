"""create config file for qjobs during installation"""

import qjobs_tmp as qjobs

if __name__ == '__main__':
    config = qjobs.config_parser()
    config.add_section('Defaults')
    for k, v in qjobs.default_config.items():
        config.set('Defaults', k, str(v))
    with open('rc_tmp', 'w') as configFile:
        config.write(configFile)
