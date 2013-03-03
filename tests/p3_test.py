from p3 import P3

import lxml
import sure

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


def test_imported():
    P3.should.be.callable


def test_instance_created():
    p3 = P3(html())
    p3.shouldnt.be.none
    p3.should.have.property("select").being.callable
    p3.should.have.property("selectAll").being.callable

