from lxml.etree import ElementBase, tostring
from lxml.html import fromstring, html_parser
from lxml.builder import ElementMaker

E = ElementMaker(makeelement=html_parser.makeelement)


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
        def _create(node, d, i):
            new = E(tag)
            node.append(new)
            return new
        return self.select(_create)

    def node(self):
        for group in self:
            for node in group:
                if node is not None:
                    return node

    def empty(self):
        return self.node is not None


class EnterSelection(BaseSelection):

    def __init__(self, ds):
        super(EnterSelection, self).__init__(ds)

    def select(self, selector):
        sel = Selection(self.dataset)
        ds = self.dataset

        for group in self:
            update = group.updates
            for i, node in enumerate(group):
                if node is not None:
                    data = ds.get(node, None)

                    subgroup = Group(
                        group.parentNode,
                        _select(group.parentNode, selector, data, i)
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

        for group in self:
            for i, node in enumerate(group):
                if node is not None:
                    data = ds.get(node, None)
                    subgroup = Group(
                        group.parentNode,
                        _select(node, selector, data, i)
                    )

                    subnode = subgroup.first

                    if subnode is not None:
                        ds[subnode] = data

                    sel.append(subgroup)
                else:
                    sel.append(None)

        return sel


    def remove(self):
        def _remove(node, d, i):
            node.getparent().remove(node)
            return node
        return self.select(_remove)

    def call(self, callable):
        callable(self)
        return self

    def each(self, callable):
        for group in self:
            for i, node in enumerate(group):
                if node is not None:
                    callable(node, self.dataset.get(node, None), i)
        return self

    def attr(self, name, val):
        def _attr(node, d, i):
            node.set(name, val if not callable(val) else val(node, d, i))
        self.each(_attr)
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


def _new_document():
    from lxml.html import builder as E
    return E.HTML(
        E.HEAD(),
        E.BODY()
    )


class P3(object):

    def __init__(self, document=None):
        self.document = document if document is not None else _new_document()
        self.dataset = {}

    def select(self, selector):
        sel = Selection(self.dataset)
        sel.append(Group(
            self.document,
            _select(self.document, selector)
        )
        )
        return sel

    def selectAll(self, selector):
        sel = Selection(self.dataset)
        sel.append(Group(
            self.document,
            _selectAll(self.document, selector)
        )
        )
        return sel
