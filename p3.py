import lxml
from lxml.etree import ElementBase
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector

html = E.HTML(
    E.HEAD(),
    E.BODY(
        E.DIV(),
        E.DIV(E.CLASS("foo")),
        E.DIV()
    )
)


class Selector(object):
    """
    encapsulates selecting
    """

    def __init__(self, node):
        self.node = node

    def __call__(self, selector, data=None, index=0, all=True):
        if callable(selector):
            return Group(self.node, [selector(self.node, data, index)])
        elif isinstance(selector, ElementBase):
            return Group(self.node, [selector])

        nodes = self.node.cssselect(selector)
        return Group(
            self.node,
            nodes if all else nodes[:1]
        )


class Group(object):
    """
    Contains nodes, and a pointer
    to the parentNode for this group
    """
    def __init__(self, parent, nodes):
        self.parentNode = parent
        self.nodes = nodes
        self.first = None
        if nodes and len(nodes):
            self.first = nodes[0]


class Selection(object):
    """
    A container of groups
    """

    def __init__(self, dataset):
        self.groups = []
        self.dataset = dataset

    def __len__(self):
        return len(self.groups)

    def selectAll(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for j, g in enumerate(self.groups):
            for i, n in enumerate(g.nodes):
                if n is not None:
                    p3_selector = Selector(n)
                    sel.groups.append(p3_selector(selector))
        return sel

    def select(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for j, g in enumerate(self.groups):
            for i, n in enumerate(g.nodes):
                if n is not None:
                    p3_selector = Selector(n)
                    data = ds.get(n, None)

                    subgroup = p3_selector(selector, data, i, all=False)
                    subnode = subgroup.first

                    if subnode is not None:
                        ds[subnode] = data

                    sel.groups.append(subgroup)
                else:
                    sel.groups.append(None)

        return sel

    def each(self, callable):
        for j, group in enumerate(self.groups):
            for i, node in enumerate(group.nodes):
                callable(node, self.dataset.get(node, None), i, j)
        return self

    def text(self, txt):
        def _text(node, d, i, j):
            node.text = txt if not callable(txt) else txt(node, d, i, j)
        self.each(_text)
        return self

    def datum(self, data=None):
        if data is None:
            return self.dataset.get(self.node(), None)

        def _datum(node, d, i, j):
            self.dataset[node] = data

        self.each(_datum)
        return self

    def data(self):
        pass

    def node(self):
        return self.groups[0].nodes[0]


class P3(object):

    def __init__(self, document):
        self.document = document
        self.data = {}

    def select(self, selector):
        sel = Selection(self.data)
        p3_selector = Selector(self.document)
        sel.groups.append(p3_selector(selector, all=False))
        return sel

    def selectAll(self, selector):
        sel = Selection(self.data)
        p3_selector = Selector(self.document)
        sel.groups.append(p3_selector(selector))
        return sel

def main():
    p3 = P3(html)

    def wibble(node, d, i, j):
        return "%s %s %s" % tuple([d, i, j])

    sel = p3.select("body").select("div")
    sel.datum("dave").text(wibble)

    print lxml.etree.tostring(html, pretty_print=True)


if __name__ == '__main__':
    main()
