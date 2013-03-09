from lxml.etree import ElementBase
from lxml.html import fromstring


def _select(node, selector, data=None, index=0):
    return _selectAll(node, selector, data=data, index=index)[:1]


def _selectAll(node, selector, data=None, index=0):
    if callable(selector):
        return [selector(node, data, index)]
    elif isinstance(selector, ElementBase):
        return [selector]
    return node.cssselect(selector)


class Group(object):
    """Contains nodes, and a pointer
    to the parentNode for this group"""
    def __init__(self, parent, nodes):
        self.parentNode = parent
        self.nodes = nodes
        self.first = None
        if nodes and len(nodes):
            self.first = nodes[0]

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, key):
        return self.nodes[key]

    def __setitem__(self, key, val):
        self.nodes[key] = val

    def __iter__(self):
        return iter(self.nodes)

    def append(self, value):
        self.nodes.append(value)


class BaseSelection(object):

    def __init__(self, dataset):
        self.groups = []
        self.dataset = dataset

    def __len__(self):
        return len(self.groups)

    def __getitem__(self, key):
        return self.groups[key]

    def __setitem__(self, key, val):
        self.groups[key] = val

    def __iter__(self):
        return iter(self.groups)

    def append(self, value):
        self.groups.append(value)

    def create(self, tag):
        def _append(node, d, i):
            new = fromstring('<%s/>' % tag)
            node.append(new)
            return new
        return self.select(_append)


class EnterSelection(BaseSelection):

    def __init__(self, ds):
        super(EnterSelection, self).__init__(ds)

    def select(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for g in self:
            update = g.updates
            for i, n in enumerate(g):
                if n is not None:
                    data = ds.get(n, None)

                    subgroup = Group(
                        g.parentNode,
                        _select(g.parentNode, selector, data, i)
                    )

                    subnode = subgroup.first
                    if subnode is not None:
                        ds[subnode] = data

                    sel.append(subgroup)
                    update[i] = subnode
                else:
                    sel.append(None)

        return sel


class Selection(BaseSelection):
    """
    A container of groups
    """

    def __init__(self, ds):
        super(Selection, self).__init__(ds)

    def selectAll(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for group in self:
            for node in group:
                if node is not None:
                    sel.append(Group(node, _selectAll(node, selector)))

        return sel

    def select(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for j, g in enumerate(self):
            for i, n in enumerate(g):
                if n is not None:

                    data = ds.get(n, None)
                    subgroup = Group(
                        g.parentNode,
                        _select(g.parentNode, selector, data, i)
                    )

                    subnode = subgroup.first

                    if subnode is not None:
                        ds[subnode] = data

                    sel.append(subgroup)
                else:
                    sel.append(None)

        return sel

    def each(self, callable):
        for j, group in enumerate(self):
            for i, node in enumerate(group):
                if node is not None:
                    callable(node, self.dataset.get(node, None), i)
        return self

    def text(self, txt):
        def _text(node, d, i):
            node.text = txt if not callable(txt) else txt(node, d, i)
        self.each(_text)
        return self

    def classed(self, cls, yesNo=None):
        def _classed(node, d, i):
            c = node.get("class", "").split()

            if cls not in c and yesNo:
                c.append(cls)
            elif cls in c and not yesNo:
                c.remove(cls)

            if len(c):
                node.set('class', ' '.join(c))
            elif 'class' in node.attrib:
                node.attrib.pop('class')

        if yesNo is None:
            return cls in node.get("class", "").split()

        self.each(_classed)
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

            for i in range(n0):
                node = group[i]
                node_data = data[i]
                if node is not None:
                    self.dataset[node] = node_data
                    updates[i] = node
                else:
                    fake = "_%d" % i
                    enters[i] = fake
                    self.dataset[fake] = node_data

            for i in range(n0, m):
                fake = "_%d" % i
                enters[i] = fake
                self.dataset[fake] = data[i]

            for i in range(m, n):
                exits[i] = group[i]

            exit.append(Group(group.parentNode, exits))

            ugroup = Group(group.parentNode, updates)
            egroup = Group(group.parentNode, enters)
            egroup.updates = ugroup

            update.append(ugroup)
            enter.append(egroup)
            enter.update = update

        enter = EnterSelection(self.dataset)
        update = Selection(self.dataset)
        exit = Selection(self.dataset)

        update.enter = lambda: enter
        update.exit = lambda: exit

        [bind(group) for group in self]

        return update

    def node(self):
        return self[0][0]


class P3(object):

    def __init__(self, document):
        self.document = document
        self.data = {}

    def select(self, selector):
        sel = Selection(self.data)
        sel.append(Group(
            self.document,
            _select(self.document, selector)
            )
        )
        return sel

    def selectAll(self, selector):
        sel = Selection(self.data)
        sel.append(Group(
            self.document,
            _selectAll(self.document, selector)
            )
        )
        return sel


def main():
    import lxml
    from lxml.html import builder as E
    from lxml.cssselect import CSSSelector

    html = E.HTML(
        E.HEAD(),
        E.BODY(
            E.DIV(),
            E.DIV(
                E.P()
            ),
            E.DIV()
        )
    )

    p3 = P3(html)

    def echo(node, d, i):
        return "%s %s" % tuple([d, i])

    sel = p3.select("body").selectAll("div").selectAll("p")

    sel = sel.data(['a', 'b', 'c', 'd', 'e'])

    sel.enter().create("p")
    sel.text(echo)

    sel.data(['a', 'b']).exit().text("gone")
    
    print(lxml.etree.tostring(html, pretty_print=True))

if __name__ == '__main__':
    main()
