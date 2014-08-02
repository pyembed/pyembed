PyEmbed
=======

.. image:: https://secure.travis-ci.org/pyembed/pyembed.png?branch=master
  :target: http://travis-ci.org/pyembed/pyembed
.. image:: https://coveralls.io/repos/pyembed/pyembed/badge.png
  :target: https://coveralls.io/r/pyembed/pyembed
.. image:: https://pypip.in/d/pyembed/badge.png
  :target: https://pypi.python.org/pypi/pyembed/
.. image:: https://pypip.in/v/pyembed/badge.png
  :target: https://pypi.python.org/pypi/pyembed/
.. image:: https://pypip.in/wheel/pyembed/badge.png
  :target: https://pypi.python.org/pypi/pyembed/
.. image:: https://pypip.in/egg/pyembed/badge.png
  :target: https://pypi.python.org/pypi/pyembed/
.. image:: https://pypip.in/license/pyembed/badge.png
  :target: https://pypi.python.org/pypi/pyembed/

`OEmbed`_ consumer library for Python with automatic discovery of
producers.

PyEmbed allows you to easily embed content on your website from a wide
variety of producers (including `Flickr`_, `Twitter`_ and `YouTube`_).
Unlike many OEmbed consumers, you don't need to configure each producer
that you want to use - PyEmbed discovers the configuration automatically.

You just need to provide the URL, and PyEmbed will generate a block of
HTML, ready for you to include in your page:

::

    >>> from pyembed.core import PyEmbed
    >>> html = PyEmbed().embed('http://www.youtube.com/watch?v=9bZkp7q19f0')
    <iframe width="480" height="270" src="http://www.youtube.com/embed/9bZkp7q19f0?feature=oembed" frameborder="0" allowfullscreen></iframe>

There are plugins for embedding content into `Markdown`_ and 
`reStructuredText`_ documents, and for customizing embeddings with `Jinja2`_
and `Mustache`_ templates.  For more information, see the `PyEmbed`_ website.

Compatibility
-------------

PyEmbed has been tested with Python 2.7 and 3.3.

Installation
------------

PyEmbed can be installed using pip:

::

    pip install pyembed

Contributing
------------

To report an issue, request an enhancement, or contribute a patch, go to
the PyEmbed `GitHub`_ page.

License
-------

PyEmbed is distributed under the MIT license.

::

    Copyright (c) 2013 Matt Thomson

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _OEmbed: http://oembed.com
.. _Flickr: http://flickr.com
.. _Twitter: http://twitter.com
.. _YouTube: http://youtube.com
.. _Markdown: https://pypi.python.org/pypi/pyembed-markdown
.. _reStructuredText: https://pypi.python.org/pypi/pyembed-rst
.. _Jinja2: https://pypi.python.org/pypi/pyembed-jinja2
.. _Mustache: https://pypi.python.org/pypi/pyembed-mustache
.. _PyEmbed: http://pyembed.github.io
.. _GitHub: https://github.com/pyembed/pyembed