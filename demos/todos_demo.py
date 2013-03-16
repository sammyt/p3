from lxml.html import builder as E
from lxml.builder import E as B

from lxml.etree import tostring
from p3 import P3

html = E.HTML(
    E.HEAD(),
    E.BODY(
        E.DIV(E.OL())
    )
)


things_to_do = [
    dict(task="wash socks", tsk_id="5321"),
    dict(task="walk dog", tsk_id="6322"),
    dict(task="read book", tsk_id="7723"),
    dict(task="potter about", tsk_id="8324")
]


def todos(selection):
    """renders todos into a selection"""
    def _copy(node, data, i):
        return data['task']

    def _link(node, data, i):
        return "/task/" + data['tsk_id']

    selection.create('a').attr('href', _link).text(_copy)


p3 = P3(html)

# set the date on the selection
sel = p3.select('ol').selectAll('li').data(things_to_do)

# create list items where needed 
sel.enter().create('li')

# use the todos callable to render the data
sel.call(todos)

print p3.html()
