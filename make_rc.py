from qjobs_tmp import *

if __name__ == '__main__':
    config = CP()
    config.add_section('Defaults')
    for k, v in default_config.items():
        config.set('Defaults', k, str(v))
    with open('rc_tmp', 'w') as configFile:
        config.write(configFile)
