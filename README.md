# qjobs

qjobs is an attempt to get a cleaner and more customizable output than the one
provided by qstat (Sun Grid Engine).

## Compatibility

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor modifications are required for
this script to work with Python 2. If needed, these modifications are
automatically made by the `install.sh` script.

## Installation

For a complete explanation of the installation process and how you can
customize it, please see [the related wiki
page](https://github.com/amorison/qjobs/wiki/Installation).

If you're already bored by the idea of wasting some RAM to open a new tab in
your browser, here is a quick explanation:

    git clone --recursive https://github.com/amorison/qjobs.git
    cd qjobs
    ./install.sh

That's it! If `~/bin` is in your PATH environment variable, you only have to
type `qjobs` to launch the wrapper. Enjoy!

If you want to uninstall `qjobs`, call the installation script with the `-u`
option: `./install.sh -u`.


## Documentation and examples

The complete documentation will be in the wiki (to do).
