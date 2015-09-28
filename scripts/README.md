buildscripts
============

This repository contains the set of helper scripts that make Seattle Testbed components executable from their source
code.   This often include copying files to the appropriate directories, cloning repositories that are needed
from Github, and setting up the tests for a repository.  Built components may be executed and tested.

The `initialize.py` and `build.py` scripts are redistributed with every buildable Seattle Testbed repository
and a "master copy" of each script (and thus the most up-to-date version) is kept here.  `initialize.py` does
a `git clone` of all the dependent repositories of a Seattle Testbed component.  `build.py` generates
runnable components out of source code that has been checked out.

[Instructions](https://seattle.poly.edu/wiki/BuildInstructions) are available that cover every step of the
Seattle Testbed build process and explain how these build scripts work.
