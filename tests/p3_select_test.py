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
            E.DIV(),
            E.DIV(E.CLASS("foo")),
            E.DIV()
        )
    )


def test_select_with_css():
    p3 = P3(html())
    sel = p3.select("div.foo")
    sel.should.be.a(Selection)
    sel.should.have.length_of(1)
    node = sel.node()
    node.get("class").should.contain("foo")


def test_select_with_callable():
    pass

def test_select_with_element():
    pass

def test_data_propogated_to_children():
    p3 = P3(html())

    d = p3.select("body").datum("wibble").select("div").datum()
    d.should.be.equal("wibble")
    
def test_data_not_propogated_without_parent():
    p3 = P3(html())

    p3.select("body").datum("wibble")

    d = p3.select("div").datum()
    d.should.be.none


