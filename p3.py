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

    def __len__(self):
        return len(self.nodes)


class BaseSelection(object):

    def append(self, tag):
        def _append(node, d, i):
            new = fromstring('<%s/>' % tag)
            node.append(new)
            return new
        return self.select(_append)


class EnterSelection(BaseSelection):
    def __init__(self, dataset):
        super(EnterSelection, self).__init__()
        self.groups = []
        self.dataset = dataset

    def select(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset
        
        for j, g in enumerate(self.groups):
            update = g.updates
            for i, n in enumerate(g.nodes):
                if n is not None:
                    p3_selector = Selector(g.parentNode)
                    data = ds.get(n, None)

                    subgroup = p3_selector(selector, data, i, all=False)
                    
                    subnode = subgroup.first
                    if subnode is not None:
                        ds[subnode] = data

                    sel.groups.append(subgroup)
                    update.nodes[i] = subnode
                else:
                    sel.groups.append(None)

        return sel


class Selection(BaseSelection):
    """
    A container of groups
    """

    def __init__(self, dataset):
        super(Selection, self).__init__()
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
                    p3_selector = Selector(g.parentNode)
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
                if node is not None:
                    callable(node, self.dataset.get(node, None), i)
        return self

    def text(self, txt):
        def _text(node, d, i):
            node.text = txt if not callable(txt) else txt(node, d, i)
        self.each(_text)
        return self

    def datum(self, data=None):
        if data is None:
            return self.dataset.get(self.node(), None)

        def _datum(node, d, i):
            self.dataset[node] = data

        self.each(_datum)
        return self

    def data(self, data=None):
        if data is None:
            return self.dataset.get(self.node(), None)

        def bind(group):
            n = len(group)
            m = len(data)
            n0 = min(n, m)
            updates = [None] * m
            enters = [None] * m
            exits = [None] * n
            end = 0

            for i in range(n0):
                node = group.nodes[i]
                node_data = data[i]
                if node is not None:
                    self.dataset[node] = node_data
                    updates[i] = node
                else:
                    fake = "_%d" % i
                    enters[i] = fake
                    self.dataset[fake] = node_data
                end = i

            for i in range(end + 1, m):
                fake = "_%d" % i
                enters[i] = fake
                self.dataset[fake] = data[i]
                end = i

            for i in range(end + 1, n):
                exits[i] = group.nodes[i]


            exit.groups.append(Group(group.parentNode, exits))
            
            ugroup = Group(group.parentNode, updates)
            egroup = Group(group.parentNode, enters)
            egroup.updates = ugroup
            
            update.groups.append(ugroup)
            enter.groups.append(egroup)
            enter.update = update

        enter = EnterSelection(self.dataset)
        update = Selection(self.dataset)
        exit = Selection(self.dataset)

        

        update.enter = lambda: enter
        update.exit = lambda: exit

        [bind(group) for group in self.groups]


        return update

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

    def out(node, d, i):
        print "%s %s" % tuple([d, i])

    def echo(node, d, i):
        return "%s %s" % tuple([d, i])

    sel = p3.select("body").selectAll("div")
    sel = sel.data(['a', 'b', 'c', 'd', 'e'])

    sel.enter().append("div")
    sel.text(echo)

    print lxml.etree.tostring(html, pretty_print=True)


if __name__ == '__main__':
    main()
