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


def test_retrieving_data():
    p3 = P3(html())
    sel = p3.selectAll("div").data(['a', 'b'])
    
    sel.data().should.equal('a')

def test_setting_data():
    p3 = P3(html())
    sel = p3.selectAll("div").data(['a', 'b'])

    sel.should.have.property("enter")
    sel.should.have.property("exit")
    sel.should.have.length_of(1)

    p3.select('div:nth-child(1)').datum().should.equal('a')
    p3.select('div:nth-child(2)').datum().should.equal('b')
    p3.select('div:nth-child(3)').datum().should.equal(None)

    enter = sel.enter()