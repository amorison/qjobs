Updating
========

If you have cloned the repository with git, updating qjobs will be very easy
and you will be able to keep your potential modifications of the installation
script. Otherwise, you will have to download a ZIP again and erase your
previous copy of qjobs. The following explanations assume you have a clone of
the git repository.

Smooth update
-------------

To update your repository, use the following command:

    git pull origin master

If everything went well, you should see at the very end of the output
a line which look like the following::

    7 files changed, 39 insertions(+), 24 deletions(-)

(where the number will vary depending on the state of your local and the remote
repositories). In this case, you just need to run the installation script to
update the installed version of qjobs: ``./install.sh``.

Minor conflict
--------------

However, as the installation script ``install.sh`` modify itself to keep your
installation settings (such as your favorite editor), a conflict may appear.
In this case, you will see the following at the end of the output::

    error: Your local changes to the following files would be overwritten by merge:
    install.sh
    Please, commit your changes or stash them before you can merge.
    Aborting

A simple way to deal with this little problem is to put away the annoying local
changes, apply the available updates, and then recover the local changes. This
is done with the following commands::

    git stash
    git merge FETCH_HEAD
    git stash pop

Finally, you just have to run the installation script to complete the update:
`./install.sh`. `More info about the stashing process`__.

.. __: https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning

For advanced users
------------------

In the case where you have modified some stuffs in the installation script
which are under the "DO NOT change anything under this line unless you know
what you are doing" line, it is very likely that some changes you made will
no longer make sense with the last version of the installation script.

After stashing the local changes and merging the fetched files, you can
see which modifications to the last version would be made if you apply
the stashed changes with the command::

    git diff -R stash

If they are many changes that are not relevant anymore, you may want to
create a new branch with the stashed version and then use the merge tools
provided by Git to recover some useful changes you made. A branch can be
created from the stash with the following command::

    git stash branch foo

where ``foo`` is the name of the created branch.

In the case where the changes you made doesn't make sense at all or you don't
want to loose time to recover them, you can erase the stashed version with::

    git stash drop
