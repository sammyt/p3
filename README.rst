P3
==

P3 contains some core features of @mbostock's awesome `d3`_ in python

Having grown used to creating html views in the browser using `d3`_. When I
came to do some server side work in python I wanted to manipulate a tree
of nodes with d3, not concatenate strings with a templating language.

P3 enables a d3 like API onto a `lxml`_ tree.

Basic Usage
-----------

Creating a simple document
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # create a new P3
    p3 = P3()

    # create some content
    p3.select('body')\
      .create('div').classed('foo', True)\
      .create('p').text('hi')

    # view the resultant HTML
    print(p3.html())  

Binding to some data
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    p3 = P3()

    # create a new unordered list
    sel = p3.select('body').create('div').create('ul')

    # bind the li elements of the list to an iterable
    sel = sel.selectAll('li').data(["foo", "bar"])

    # create li elements required to display the data
    sel.enter().create('li')

    # pass a callable to text inorder to update each
    # li with a value based of its datum
    sel.text(lambda n, d, i: d)

    print(p3.html())

.. _d3: http://d3js.org/
.. _lxml: http://lxml.de