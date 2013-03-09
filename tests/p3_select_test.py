from p3 import P3, Selection

import lxml
import sure

from lxml.etree import ElementBase
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector


def html():
    return E.HTML(
        E.HEAD(),
        E.BODY(
            E.DIV(E.CLASS('first')),
            E.DIV(E.CLASS('second'))
        )
    )

def create():
    return P3(html())


def test_select_first_match():
    doc = html()
    p3 = P3(doc)
    div = p3.select('div')

    node = doc.cssselect('.first')[0]
    div[0][0].should.equal(node)


def test_propogates_parent_node():
    doc = html()
    p3 = P3(doc)
    sel = p3.select('div')

    sel[0].parentNode.shouldnt.be.none
    sel[0].parentNode.should.equal(doc)


def test_propogates_data_to_selected_elements():
    data = dict(foo='bar')
    doc = html()
    p3 = P3(doc)

    div = p3.select('body').data([data]).select('div')

    node_data = p3.dataset[div[0][0]]
    node_data.should.eql(data)


def test_select_with_css():
    p3 = P3(html())
    sel = p3.select('div.first')
    sel.should.be.a(Selection)
    sel.should.have.length_of(1)
    node = sel.node()
    node.get('class').should.contain('first')


def test_select_with_callable():
    def callme(node, data, index):
        node.should.be.a(ElementBase)
        data.should.be.none
        index.should.equal(0)
        return p3.select('div').node()

    p3 = P3(html())
    n = p3.select(callme).node()
    n.shouldnt.none

    p3.select('div').node().should.be.equal(n)


def test_select_with_element():
    p3 = P3(html())
    n = p3.select('.first').node()
    n.shouldnt.none

    p3.select(n).node().should.equal(n)

def test_data_propogated_to_children():
    p3 = P3(html())

    d = p3.select("body").datum("wibble").select("div").datum()
    d.should.be.equal("wibble")
    
def test_data_not_propogated_without_parent():
    p3 = P3(html())

    p3.select("body").datum("wibble")

    d = p3.select("div").datum()
    d.should.be.none


