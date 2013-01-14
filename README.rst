=======================
djangorestframework-csv
=======================

|build status|_

.. |build status| image:: https://secure.travis-ci.org/mjumbewu/django-rest-framework-csv.png
.. _build status: https://secure.travis-ci.org/mjumbewu/django-rest-framework-csv

**CSV Tools for Django REST Framework**

**Author:** Mjumbe Wawatu Poe, `Follow me on Twitter <http://www.twitter.com/mjumbewu>`_.

Usage
-----

*views.py*::

    from rest_framework.views import APIView
    from rest_framework.settings import api_settings
    from rest_framework_csv import CSVRenderer

    class MyView (APIView):
        renderer_classes = (CSVRenderer, ) + api_settings.DEFAULT_RENDERER_CLASSES
        ...

For more information about using renderers with Django REST Framework, see the
`API Guide <http://django-rest-framework.org/api-guide/renderers.html>`_ or the
`Tutorial <http://django-rest-framework.org/tutorial/1-serialization.html>`_.

Running the tests
-----------------

To run the tests against the current environment:

    ./manage.py test


Changelog
=========

1.0.1
-----

* Add the package manifest

1.0.0
-----

* Initial release


License
=======

Copyright © Mjumbe Wawatu Poe.

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
