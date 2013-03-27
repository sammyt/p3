P3
==

P3 contains some core features of @mbostock's awesome `d3`_ in python.

Rational
--------

Using `d3`_ on a daily basis I'm now most comfortable driving the DOM with data.
When I came to do some server side work in python I missed d3's abstractions, 
and felt uncomfortable concatenating strings with templating languages. 

P3 ports much of d3's core library for manipulating documents to python.

The document itself is provided by `lxml`_

Installation
------------

.. code:: none

    pip install p3



Getting Started
---------------

Creating a P3 instance
~~~~~~~~~~~~~~~~~~~~~~

Import the P3 class from p3

.. code:: python

    from p3 import P3


Create a new P3 instance with no args.

.. code:: python

    p3 = P3()
    print(p3.html())

calling .html outputs the document associated with this p3 instance. Here the
the default empty document is displayed.

.. code:: html

    <!doctype html>
    <html>
        <head></head>
        <body></body>
    </html>


You might already have a document though, in which case just pass it into
the constructor

.. code:: python

    from lxml.html import builder as E
    from p3 import P3

    doc = E.HTML(
        E.HEAD(),
        E.BODY(
            E.DIV(E.OL())
        )
    )

    p3 = P3(doc)
    print(p3.html())


.. code:: html

    <!doctype html>
    <html>
        <head></head>
        <body>
            <div>
                <ol></ol>
            </div>
        </body>
    </html>


Driving the document with data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    teas = [
        'breakfast',
        'darjeeling',
        'earl grey',
        'peppermint'
    ]

    p3 = P3()

    sel = p3.select('body').create('div').classed('container', True)
    sel = sel.create('ul')

    update = sel.select_all('ul').data(teas)
    update.enter().create('ul')

    update.text(lambda n, d, i: "lovely %s tea" % d)

    print(p3.html())


.. code:: html

    <!doctype html>
    <html>
        <head></head>
        <body>
            <div class="container">
                <ul>
                    <li>lovely breakfast tea</li>
                    <li>lovely darjeeling tea</li>
                    <li>lovely earl grey tea</li>
                    <li>lovely peppermint tea</li>
                </ul>
            </div>
        </body>
    </html>



.. _d3: http://d3js.org/
.. _lxml: http://lxml.de