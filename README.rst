.. image:: https://readthedocs.org/projects/qjobs/badge/?version=latest
    :target: http://qjobs.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


qjobs
=====

qjobs is an attempt to get a cleaner and more customizable output than the one
provided by qstat (Sun Grid Engine).

Quick installation
------------------

``qjobs`` only uses built-in Python modules. It is compatible with Python3.4
and higher.

Installation of ``qjobs`` can be done with ``setuptools``. ::

    git clone https://github.com/amorison/qjobs.git
    cd qjobs
    python3 setup.py install --user

That's it! If the directory where setuptools installs packages (usually
``~/.local/bin``) is in your ``PATH`` environment variable, you only have to
run ``qjobs`` from the command line to launch the wrapper. Enjoy!
