#!/bin/sh

pathScript=$HOME'/bin'
scriptFile='qjobs'
pathConfig=$HOME'/.config/qjobs'
configFile='qjobs.rc'
pythonCmd=''
pythonVersion=0

#############################################################################
# DO NOT change anything under this line unless you know what you are doing #
#############################################################################

\cp qjobs.py qjobs_tmp

echo 'Looking for Python...'

if [ -z "$pythonCmd" ]; then
    pythonCmd=`command -v python3`
    if [ -z "$pythonCmd" ]; then
        pythonCmd=`command -v python2`
        if [ -z "$pythonCmd" ]; then
            pythonVersion=0
        else
            pythonVersion=2
        fi
    else
        pythonVersion=3
    fi
fi

if [ "$pythonVersion" -eq "0" ]; then
    echo 'Python not found, please set pythonCmd and pythonVersion variables.'
    exit 1
fi

echo 'Python '$pythonVersion' found at '$pythonCmd

if [ "$pythonVersion" -eq "2" ]; then
    \sed -i '1 a from __future__ import print_function' qjobs_tmp
    \sed -i 's/import configparser/import ConfigParser as configparser/' qjobs_tmp
    \sed -i 's/ConfigParser()/SafeConfigParser()/' qjobs_tmp
    echo 'script modified for compatibility'
fi

echo ''

\mkdir -p $pathScript
\mkdir -p $pathConfig

pathScript=$pathScript'/'$scriptFile
pathConfig=$pathConfig'/'$configFile

\sed -i 's!PYTHON_CMD!'$pythonCmd'!' qjobs_tmp
\sed -i 's!PATH_CONFIG!'$pathConfig'!' qjobs_tmp
\sed -i 's/USER_NAME/'$USER'/' qjobs_tmp

echo 'user name found: '$USER

echo ''

\chmod u+x qjobs_tmp
echo 'qjobs will be installed at '$pathScript' ...'
\mv qjobs_tmp $pathScript
echo '...done.'

echo 'config file will be copied at '$pathConfig' ...'
\cp qjobs.rc $pathConfig
echo '...done.'

echo ''

echo 'Installation finished!'