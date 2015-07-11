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

\cp "$0" install_cp

instdest=$HOME'/.local/share/qjobs'
echo 'copy sources files to '$instdest
echo '...'
mkdir -p $instdest
\rm -rf $instdest/*
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

\sed -i "s!^qstatCmd=.*!qstatCmd='$qstatCmd'!" install_cp

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
else
    echo 'Python already set'
fi

if [ "$pythonVersion" -eq "0" ]; then
    echo 'Python not found, please enter its location:'
    \read -r pythonCmd
    echo 'and the version number (2 or 3):'
    \read -r pythonVersion
fi

echo 'will use Python '$pythonVersion' at '$pythonCmd

\sed -i "s!^pythonCmd=.*!pythonCmd='$pythonCmd'!" install_cp
\sed -i "s!^pythonVersion=.*!pythonVersion=$pythonVersion!" install_cp

if [ "$pythonVersion" -eq "2" ]; then
    \sed -i '3 a from __future__ import print_function' $instdest/main.py
    \sed -i '2 a from __future__ import print_function' $instdest/cmdargs.py
    \sed -i '2 a from __future__ import print_function' $instdest/configfile.py
    \sed -i '2 a from __future__ import print_function' $instdest/output.py
    \sed -i 's/ConfigParser/SafeConfigParser/' $instdest/configfile.py
    \sed -i 's/configparser/ConfigParser/' $instdest/configfile.py
    \sed -i 's/configparser/ConfigParser/' $instdest/main.py
    \sed -i 's/zip_longest/izip_longest/' $instdest/output.py
    \sed -i 's/input(/raw_input(/' $instdest/cmdargs.py
    echo 'sources modified for compatibility with Python 2'
fi

echo ''

\mkdir -p $pathScript
\mkdir -p $pathConfig

pathScript=$pathScript'/'$scriptFile
pathConfig=$pathConfig'/'$configFile

\sed -i 's!QSTAT_CMD!'$qstatCmd'!' $instdest/constants.py
\sed -i 's!PYTHON_CMD!'$pythonCmd'!' $instdest/main.py
\sed -i 's!PATH_CONFIG!'$pathConfig'!' $instdest/constants.py
\sed -i 's/USER_NAME/'$USER'/' $instdest/constants.py
\sed -i 's!EDITOR!'$editor'!' $instdest/constants.py
\chmod u+x $instdest/main.py

echo 'user name found: '$USER
echo 'editor set to: '$editor

echo ''

$pythonCmd $instdest/main.py -c > rc_tmp
\mv rc_tmp $pathConfig

echo 'config file created at '$pathConfig':'
\cat $pathConfig

echo 'linking '$pathScript' ...'
\ln -s -f $instdest/main.py $pathScript
echo 'done.'

echo ''

echo 'Installation finished!'
\mv install_cp "$0"
