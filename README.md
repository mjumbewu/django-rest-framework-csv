Django Reusable Apps
====================

**Simple template for reusable apps with Django.**

**Author:** Tom Christie, [Follow me on Twitter][1].

Overview
========

A simple template for creating reusable apps with Django.

Includes:

1. A `setup.py` that makes your life easy and doesn't suck.
2. A simple layout that lets you run the app's tests without installing it into an existing project.
3. A `tox` config to allow you to run your tests against multiple environments.

Creating a new app
==================

You'll want to clone this project, then create a fresh git repo for it:

    git clone git://github.com/dabapps/django-reusable-app.git my-project-name
    cd my-project-name
    mv myproject packagename
    rm -rf .git
    git init

Edit `testsettings.py` and update the app name in INSTALLED_APPS.
Edit `setup.py` and update the settings at the top of the file.
Edit the `README`.

Pushing releases to PyPI
========================

To register your package on PyPI:

    ./setup.py register

To publish a new version of your app to PyPI, set the `__version__` string in
your package's `__init__.py`, then run:

    ./setup.py publish

Running the tests
=================

To run the tests against the current environment:

    ./manage.py test

To run the tests against multiple environments, install `tox` using
`pip install tox`, make sure you're not currently in a virtual environment,
then simply run `tox`:

    tox

Changelog
=========

1.0.1
-----

* Include author_email in setup.py
* Move testsettings into top level dir
* Update tox to test against Django 1.3, 1.4 (From 1.2, 1.3)

1.0.0
-----

* Initial release

License
=======

Copyright © DabApps.

All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[1]: http://twitter.com/_tomchristie
