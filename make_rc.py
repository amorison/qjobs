from qjobs_tmp import *

if __name__ == '__main__':
    config = CP()
    config['Defaults'] = default_config
    with open('rc_tmp','w') as configFile:
        config.write(configFile)
