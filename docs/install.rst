Installation
============

Downloading
-----------

First, you need to get a copy of this GitHub repository. You can download an
archive with the [Download
ZIP](https://github.com/amorison/qjobs/archive/master.zip) button on the main
page.

However, cloning the actual git repository will allow you to keep your copy
up-to-date more easily. See the [Update page of this
wiki](https://github.com/amorison/qjobs/wiki/Update). I tried to explain things
clearly even for a git-newbie. I hope that goal is achieved, please let me know
if this isn't the case.  If you don't know at all what git is (or if you need a
quick reminder), [the first chapter of the Git
book](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
should give you the necessary basis to understand what is going on.

To clone the repository, use the following command:

    git clone --recursive https://github.com/amorison/qjobs.git

The `--recursive` option asks git to "clone" also submodules, useful here to
get a local copy of the wiki. You can omit it if you don't want to copy the
wiki locally. If you change your mind and want to add the wiki to an existing
clone, run the following commands:

    git submodule init
    git submodule update

[More info about
submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

If you want to [use the SSH
protocol](https://help.github.com/articles/generating-ssh-keys/) instead of
https, use this command to perform the clone:

    git clone --recursive git@github.com:amorison/qjobs.git

Installation - Uninstallation
-----------------------------

Anyway, the cloning will create a `qjobs` directory in your current directory,
which is our next destination:

    cd qjobs

If everything went well, you should see an installation script named `install.sh`.
You can run it immediately, or take a look at the [customization
instructions](https://github.com/amorison/qjobs/wiki/Installation#customization).

    ./install.sh

To uninstall `qjobs`, use the `-u` option of the same script:

    ./install.sh -u

Customization
-------------

By default, the installation script does the following:

- creates a `qjobs` directory in `~/.local/share` where the Python modules are
  copied;
- creates a `qjobs` directory in `~/.config` where the default config file is
  put;
- creates a symbolic link named `qjobs` in `~/bin` which points toward the main
  module in `~/.local/share`.

You can customize the installation process by editing the first lines of the
script before running it.

The variable `linkDir` is the directory where the link to the main module
will be created.  Its default value is `~/bin`. You may want to choose a
directory which is in your path.

The variable `linkName` is the name of the said link. Its default value is
`'qjobs'`. Hence, if `pathScript` is in your path, you will only need to type
`qjobs` to launch the program.

The variable `installDir` is the name of the directory where the Python modules
will be copied. Its default value is `~/.local/share`.

The variable `configDir` is the name of the directory where the config file
will be copied. Its default value is `~/.config`.

You can force the location of the `qstat` program with the `qstatCmd` variable.

You can set the editor which will be used to edit the config file with the `-e`
option with the `editor` variable.

If you already have a config file which set the value of `qstat_cmd` and/or
`editor`, these values replace the ones specified in the install script for
`qstatCmd` and/or `editor`.

Finally, you can also force the location of the Python interpretor with the
`pythonCmd` and `pythonVersion` variables. For example, if you have a fancy
Python 2 interpretor located in `/opt/bin/myPython`, you could force its use
by setting `pythonCmd='/opt/bin/myPython'` and `pythonVersion=2`. In most
cases, you don't need to bother with these variables as the installation script
will look for a Python interpretor in your path (and adapt the script to Python
2 if needed).
