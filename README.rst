REmbed
======

.. image:: https://secure.travis-ci.org/matt-thomson/rembed.png?branch=master
    :target: http://travis-ci.org/matt-thomson/rembed

`OEmbed`_ consumer library for Python with automatic discovery of
producers.

REmbed allows you to easily embed content on your website from a wide
variety of producers (including `Flickr`_, `Twitter`_ and `YouTube`_).
Unlike many OEmbed consumers, you don't need to configure each producer
that you want to use - REmbed discovers the configuration automatically.

You just need to provide the URL, and REmbed will generate a block of
HTML, ready for you to include in your page:

::

    >>> from rembed import consumer
    >>> consumer.embed('http://www.youtube.com/watch?v=9bZkp7q19f0')
    <iframe width="480" height="270" src="http://www.youtube.com/embed/9bZkp7q19f0?feature=oembed" frameborder="0" allowfullscreen></iframe>

Installation
------------

REmbed can be installed using pip:

::

    pip install rembed

Contributing
------------

To report an issue, request an enhancement, or contribute a patch, go to
the REmbed `GitHub`_ page.

.. _OEmbed: http://oembed.com
.. _Flickr: http://flickr.com
.. _Twitter: http://twitter.com
.. _YouTube: http://youtube.com
.. _GitHub: https://github.com/matt-thomson/rembed