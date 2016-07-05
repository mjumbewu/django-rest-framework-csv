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
`settings.py` file:

.. code-block:: python

    REST_FRAMEWORK = {
        # specifying the renderers
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_csv.renderers.CSVRenderer',
        ),
    }

Ordered Fields
--------------

By default, a ``CSVRenderer`` will output fields in sorted order. To specify
an alternative field ordering you can override the ``header`` attribute. There
are two ways to do this:

1) Create a new renderer class and override the ``header`` attribute directly:

    .. code-block:: python

        class MyUserRenderer (CSVRenderer):
            header = ['first', 'last', 'email']

        @api_view(['GET'])
        @renderer_classes((MyUserRenderer,))
        def my_view(request):
            users = User.objects.filter(active=True)
            content = [{'first': user.first_name,
                        'last': user.last_name,
                        'email': user.email}
                       for user in users]
            return Response(content)

2) Use the ``renderer_context`` to override the field ordering on the fly:

    .. code-block:: python

        class MyView (APIView):
            renderer_classes = [CSVRenderer]

            def get_renderer_context(self):
                context = super().get_renderer_context()
                context['header'] = (
                    self.request.GET['fields'].split(',')
                    if 'fields' in self.request.GET else None)
                return context

            ...

Labeled Fields
--------------

Custom labels can be applied to the ``CSVRenderer`` using the ``labels`` dict
attribute where each key corresponds to the header and the value corresponds
to the custom label for that header.

1) Create a new renderer class and override the ``header`` and ``labels``
attribute directly:

    .. code-block:: python

        class MyBazRenderer (CSVRenderer):
            header = ['foo.bar']
            labels = {
                'foo.bar': 'baz'
            }

Pagination
----------

Using the renderer with paginated data is also possible, with a little extension.
A paginated CSV renderer is constructed like below, and should be used with views
that paginate data

.. code-block:: python

    from rest_framework_csv.renderers import CSVRenderer

    class PaginatedCSVRenderer (CSVRenderer):
        results_field = 'results'

        def render(self, data, *args, **kwargs):
            if not isinstance(data, list):
                data = data.get(self.results_field, [])
            return super(PaginatedCSVRenderer, self).render(data, *args, **kwargs)

For more information about using renderers with Django REST Framework, see the
`API Guide <http://django-rest-framework.org/api-guide/renderers/>`_ or the
`Tutorial <http://django-rest-framework.org/tutorial/1-serialization/>`_.

Running the tests
-----------------

To run the tests against the current environment:

.. code-block:: bash

    $ ./manage.py test


Changelog
=========

1.4.0/1.4.1
-----------

- Add support for changing field labels in the ``CSVRenderer``, thanks to @soby
- Add support for setting ``CSVRenderer`` headers, labels, and writer_opts as
  ``renderer_context`` parameters.
- Renamed ``CSVRenderer.headers`` to ``CSVRenderer.header``; old spelling is
  still available for backwards compatibility, but may be removed in the future.

1.3.4
-----

- Support streaming CSV rendering, via @ivancrneto
- Improved test configuration and project metadata, via @ticosax

1.3.2/1.3.3
-----------

- Support unicode CSV parsing, and universal newlines, with thanks to @brocksamson

1.3.1
-----

- Renderer handles case where data is not a list by wrapping data in a list, via pull request from @dougvk
- Better cross Python version support, via @paurullan and @vishen

1.3.0
-----

- Support for Python 3, derived from work by @samdobson

1.2.0
-----

- Support consistent ordering of fields in rendered CSV; thanks to @robguttman
- Support specifying particular fields/headers in custom CSV renderer by
  overriding the ``headers`` attribute.

1.1.0
-----

- Support simple CSV parsing; thanks to @sebastibe

1.0.1
-----

- Add the package manifest

1.0.0
-----

- Initial release


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
