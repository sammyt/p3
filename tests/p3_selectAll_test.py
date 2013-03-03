from p3 import P3, Selection
from lxml.html import builder as E
import sure


def html():
    return E.HTML(
        E.HEAD(),
        E.BODY(
            E.DIV(),
            E.DIV(E.CLASS("foo")),
            E.DIV(E.P())
        )
    )


def test_selectAll_with_css():
    p3 = P3(html())
    sel = p3.selectAll("div")
    sel.should.be.a(Selection)
    sel.should.have.length_of(1)

    sel = sel.selectAll("p")
    sel.should.have.length_of(3)

    sel.groups[0].nodes.should.be.empty
    sel.groups[1].nodes.should.be.empty
    sel.groups[2].nodes.shouldnt.be.empty

