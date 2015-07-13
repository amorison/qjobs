#!/bin/sh

# name and location of link
linkDir="$HOME/bin"
linkName='qjobs'

# installation directories
installDir="$HOME/.local/share"
configDir="$HOME/.config"

# tools location
qstatCmd=
pythonCmd=
pythonVersion=0
editor=

#############################################################################
# DO NOT change anything under this line unless you know what you are doing #
#############################################################################

pathConfig="$configDir/qjobs"
instdest="$installDir/qjobs"

uflag=
while getopts u name
do
    case $name in
        u)   uflag=1;;
        ?)   echo '-u to uninstall'
             exit 1;;
    esac
done

if [ ! -z "$uflag" ]; then
    echo 'uninstalling...'
    echo 'removing link'
    \rm $linkDir/$linkName
    echo 'removing config file'
    \rm -rf $pathConfig
    echo 'removing source files'
    \rm -rf $instdest
    echo 'done.'
    exit 0
fi

echo "copy sources files to $instdest"
mkdir -p $instdest
\rm -rf $instdest/*
\cp src/* $instdest
echo 'done.'

echo ''

if [ -z "$qstatCmd" ]; then
    echo 'looking for qstat...'
    qstatCmd=`command -v qstat`
    if [ -z "$qstatCmd" ]; then
        echo 'qstat not found, please enter its location:'
        \read -r qstatCmd
    fi
else
    echo 'qstat already set'
fi

echo "will use $qstatCmd"

echo ''

echo 'looking for Python...'

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

echo "will use $pythonCmd (Python $pythonVersion)"


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

usrnm=$USER
if [ -z "$usrnm" ]; then
    echo 'user name not found, please enter yours:'
    \read -r usrnm
fi
echo 'user name set as: '$usrnm

echo ''

if [ -z "$editor" ]; then
    echo 'please choose an editor (leave empty for vim):'
    \read -r editor
    if [ -z "$editor" ]; then
        editor='vim'
    fi
fi
echo 'editor set as: '$editor

\mkdir -p $linkDir
\mkdir -p $pathConfig

linkDir="$linkDir/$linkName"
pathConfig="$pathConfig/qjobs.rc"

\sed -i "s!QSTAT_CMD!$qstatCmd!" $instdest/constants.py
\sed -i "s!PYTHON_CMD!$pythonCmd!" $instdest/main.py
\sed -i "s!PATH_CONFIG!$pathConfig!" $instdest/constants.py
\sed -i "s/USER_NAME/$USER/" $instdest/constants.py
\sed -i "s!EDITOR!$editor!" $instdest/constants.py
\chmod u+x $instdest/main.py

echo ''

$pythonCmd $instdest/main.py -c > rc_tmp
\mv rc_tmp $pathConfig

echo "config file created at $pathConfig:"
\cat $pathConfig

echo "linking $linkDir"
\ln -s -f $instdest/main.py $linkDir
echo 'done.'

echo ''

echo 'installation finished!'

echo ''

\cp "$0" install_cp

\sed -i "s!^qstatCmd=.*!qstatCmd='$qstatCmd'!" install_cp
\sed -i "s!^pythonCmd=.*!pythonCmd='$pythonCmd'!" install_cp
\sed -i "s!^pythonVersion=.*!pythonVersion=$pythonVersion!" install_cp
\sed -i "s!^editor=.*!editor='$editor'!" install_cp

\mv install_cp "$0"

echo 'install script updated'
