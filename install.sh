#!/usr/bin/sh

pathScript=$HOME'/bin'
pathConfig=$HOME'/.config/qjobs'
configFile='qjobs.rc'


# DO NOT change anything under this line unless you know what you are doing
############################################################################

\mkdir -p $pathScript
\mkdir -p $pathConfig

pathConfig=$pathConfig'/'$configFile
\sed -i 's!RUN_INSTALL!'$pathConfig'!' qjobs
\chmod u+x qjobs

\cp qjobs $pathScript
\cp qjobs.rc $pathConfig
