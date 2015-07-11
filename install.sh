#!/bin/sh

pathScript=$HOME'/bin'
scriptFile='qjobs'
pathConfig=$HOME'/.config/qjobs'
configFile='qjobs.rc'
qstatCmd=''
pythonCmd=''
pythonVersion=0
editor='vim'

#############################################################################
# DO NOT change anything under this line unless you know what you are doing #
#############################################################################

instdest=$HOME'/.local/share/qjobs'
echo 'copy sources files to '$instdest
echo '...'
mkdir -p $instdest
\cp src/* $instdest
echo 'done.'

echo ''

if [ -z "$qstatCmd" ]; then
    echo 'Looking for qstat...'
    qstatCmd=`command -v qstat`
    if [ -z "$qstatCmd" ]; then
        echo 'qstat not found, please enter its location:'
        \read -r qstatCmd
    fi
    echo 'will use '$qstatCmd' as qstat'
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
    echo 'Python not found, please enter its location:'
    \read -r pythonCmd
    echo 'and the version number (2 or 3):'
    \read -r pythonVersion
fi

echo 'will use Python '$pythonVersion' at '$pythonCmd

if [ "$pythonVersion" -eq "2" ]; then
    \sed -i '3 a from __future__ import print_function' $instdest/qjobs.py
    \sed -i 's/ConfigParser/SafeConfigParser/' $instdest/qjobs.py
    \sed -i 's/configparser/ConfigParser/' $instdest/qjobs.py
    \sed -i 's/zip_longest/izip_longest/' $instdest/qjobs.py
    echo 'script modified for compatibility'
fi

echo ''

\mkdir -p $pathScript
\mkdir -p $pathConfig

pathScript=$pathScript'/'$scriptFile
pathConfig=$pathConfig'/'$configFile

\sed -i 's!QSTAT_CMD!'$qstatCmd'!' $instdest/constants.py
\sed -i 's!PYTHON_CMD!'$pythonCmd'!' $instdest/qjobs.py
\sed -i 's!PATH_CONFIG!'$pathConfig'!' $instdest/constants.py
\sed -i 's/USER_NAME/'$USER'/' $instdest/constants.py
\sed -i 's/EDITOR/'$editor'/' $instdest/constants.py
\chmod u+x $instdest/qjobs.py

echo 'user name found: '$USER

echo ''

$pythonCmd $instdest/qjobs.py -c > $pathConfig

echo 'config file created at '$pathConfig':'
\cat $pathConfig

echo 'linking '$pathScript' ...'
\ln -s -f $instdest/qjobs.py $pathScript
echo 'done.'

echo ''

echo 'Installation finished!'
