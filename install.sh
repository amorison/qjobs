#!/bin/sh

pathScript=$HOME'/bin'
scriptFile='qjobs'
pathConfig=$HOME'/.config/qjobs'
configFile='qjobs.rc'
qstatCmd=''
pythonCmd=''
pythonVersion=0

#############################################################################
# DO NOT change anything under this line unless you know what you are doing #
#############################################################################

instdest=$HOME'/.local/share/qjobs'
mkdir -p $instdest
\cp src/* $instdest
instdest=$instdest'/qjobs.py'

if [ -z "$qstatCmd" ]; then
    echo 'Looking for qstat...'
    qstatCmd=`command -v qstat`
    if [ -z "$qstatCmd" ]; then
        echo 'qstat not found, please set qstatCmd variables.'
        exit 1
    fi
    echo 'qstat found at '$qstatCmd
else
    echo 'qstat already set at '$qstatCmd
fi

echo ''

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
    \sed -i '3 a from __future__ import print_function' $instdest
    \sed -i 's/ConfigParser/SafeConfigParser/' $instdest
    \sed -i 's/configparser/ConfigParser/' $instdest
    \sed -i 's/zip_longest/izip_longest/' $instdest
    echo 'script modified for compatibility'
fi

echo ''

\mkdir -p $pathScript
\mkdir -p $pathConfig

pathScript=$pathScript'/'$scriptFile
pathConfig=$pathConfig'/'$configFile

\sed -i 's!QSTAT_CMD!'$qstatCmd'!' $instdest
\sed -i 's!PYTHON_CMD!'$pythonCmd'!' $instdest
\sed -i 's!PATH_CONFIG!'$pathConfig'!' $instdest
\sed -i 's/USER_NAME/'$USER'/' $instdest
\chmod u+x $instdest

echo 'user name found: '$USER

echo ''

$pythonCmd $instdest -c > rc_tmp

echo 'config file created:'
\cat rc_tmp

echo 'qjobs will be installed as '$pathScript' ...'
\ln -s -f $instdest $pathScript
echo '...done.'

echo 'config file will be moved to '$pathConfig' ...'
\mv rc_tmp $pathConfig
echo '...done.'

echo ''

echo 'Installation finished!'
