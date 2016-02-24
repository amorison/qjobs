.. image:: https://readthedocs.org/projects/qjobs/badge/?version=latest
    :target: http://qjobs.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status


qjobs
=====

qjobs is an attempt to get a cleaner and more customizable output than the one
provided by qstat (Sun Grid Engine).

Compatibility
-------------

qjobs only uses built-in Python modules.

qjobs is developed with Python 3, but only minor modifications are required for
this script to work with Python 2. If needed, these modifications are
automatically made by the ``install.sh`` script.

For Python 3, the required version is 3.2 or later. For Python 2, the required
version is 2.7.

Quick installation
------------------

For a complete explanation of the installation process and how you can
customize it, please see the documentation.

If you're already bored by the idea of wasting some RAM to open a new tab in
your browser, here is a hurry-geek-friendly explanation::

    git clone https://github.com/amorison/qjobs.git
    cd qjobs
    ./install.sh

That's it! If ``~/bin`` is in your PATH environment variable, you only have to
type ``qjobs`` to launch the wrapper. Enjoy!

If you want to uninstall ``qjobs``, call the installation script with the
``-u`` (as in "unlikely") option: ``./install.sh -u``.
