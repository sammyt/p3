P3
==

P3 contains some core features of @mbostock's awesome `d3`_ in python

Why
---

I have grown used to creating html views in the browser using d3. When I
came to do some server side work in python I wanted to manipulate a tree
of nodes with d3, not concatenate strings with a templating language.

Basic Usage
-----------

Creating a simple document
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    p3 = P3()
    p3.select('body')\
      .create('div').classed('foo', True)\
      .create('p').text('hi')

Binding to some data
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    p3 = P3()

    sel = p3.select('body').create('div').create('ul')
    sel = sel.selectAll('li').data(["foo", "bar"])
    sel.enter().create('li')
    sel.text(lambda n, d, i: d)

.. _d3: http://d3js.org/