REmbed
======

.. image:: https://secure.travis-ci.org/matt-thomson/rembed.png?branch=master
    :target: http://travis-ci.org/matt-thomson/rembed
.. image:: https://coveralls.io/repos/matt-thomson/rembed/badge.png
    :target: https://coveralls.io/r/matt-thomson/rembed
.. image:: https://pypip.in/v/rembed/badge.png
    :target: https://crate.io/packages/rembed/
.. image:: https://pypip.in/d/rembed/badge.png
    :target: https://crate.io/packages/rembed/

`OEmbed`_ consumer library for Python with automatic discovery of
producers.

REmbed allows you to easily embed content on your website from a wide
variety of producers (including `Flickr`_, `Twitter`_ and `YouTube`_).
Unlike many OEmbed consumers, you don't need to configure each producer
that you want to use - REmbed discovers the configuration automatically.

You just need to provide the URL, and REmbed will generate a block of
HTML, ready for you to include in your page:

::

    >>> from rembed.core import consumer
    >>> consumer.embed('http://www.youtube.com/watch?v=9bZkp7q19f0')
    <iframe width="480" height="270" src="http://www.youtube.com/embed/9bZkp7q19f0?feature=oembed" frameborder="0" allowfullscreen></iframe>

Compatibility
-------------

REmbed has been tested with Python 2.7 and 3.3.

Installation
------------

REmbed can be installed using pip:

::

    pip install rembed

Contributing
------------

To report an issue, request an enhancement, or contribute a patch, go to
the REmbed `GitHub`_ page.

License
-------

REmbed is distributed under the MIT license.

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
.. _GitHub: https://github.com/matt-thomson/rembed