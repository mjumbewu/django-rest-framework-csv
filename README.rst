=======================
djangorestframework-csv
=======================

|build status|_

.. |build status| image:: https://secure.travis-ci.org/mjumbewu/django-rest-framework-csv.png
.. _build status: https://travis-ci.org/mjumbewu/django-rest-framework-csv

**CSV Tools for Django REST Framework**

**Author:** Mjumbe Wawatu Poe, `Follow me on Twitter <http://www.twitter.com/mjumbewu>`_.

Installation
------------

.. code-block:: bash

    $ pip install djangorestframework-csv

Usage
-----

*views.py*

.. code-block:: python

    from rest_framework.views import APIView
    from rest_framework.settings import api_settings
    from rest_framework_csv import renderers as r

    class MyView (APIView):
        renderer_classes = (r.CSVRenderer, ) + api_settings.DEFAULT_RENDERER_CLASSES
        ...

Alternatively, to set CSV as a default rendered format, add the following to the 
`settings.py` file::

    REST_FRAMEWORK = {
        # specifying the renderers
        'DEFAULT_RENDERER_CLASSES': (            
            'rest_framework_csv.renderers.CSVRenderer', 
        ),
    }

Pagination
----------

Using the renderer with paginated data is also possible, with a little extension.
A paginated CSV renderer is constructed like below, and should be used with views
that paginate data::

    from rest_framework_csv.renderers import CSVRenderer
    
    class PaginatedCSVRenderer (CSVRenderer):
        results_field = 'results'
    
        def render(self, data, media_type=None, renderer_context=None):
            if not isinstance(data, list):
                data = data.get(self.results_field, [])
            return super(PaginatedCSVRenderer, self).render(data, media_type, renderer_context)

For more information about using renderers with Django REST Framework, see the
`API Guide <http://django-rest-framework.org/api-guide/renderers.html>`_ or the
`Tutorial <http://django-rest-framework.org/tutorial/1-serialization.html>`_.

Running the tests
-----------------

To run the tests against the current environment:

.. code-block:: bash

    $ ./manage.py test


Changelog
=========

1.3.0
-----

* Support for Python 3, derived from work by @samdobson

1.2.0
-----

* Support consistent ordering of fields in rendered CSV; thanks to @robguttman
* Support specifying particular fields/headers in custom CSV renderer by 
  overriding the ``headers`` attribute.

1.1.0
-----

* Support simple CSV parsing; thanks to @sebastibe

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
