from lxml.etree import ElementBase
from lxml.html import fromstring, html_parser, tostring
from lxml.builder import ElementMaker
from uuid import uuid4
import collections


E = ElementMaker(makeelement=html_parser.makeelement)


def _select(node, selector, data=None, index=0):
    sel = _selectAll(node, selector, data=data, index=index)[:1]
    return None if len(sel) == 0 else sel[0]


def _selectAll(node, selector, data=None, index=0):
    if callable(selector):
        ans = selector(node, data, index)
        return ans if isinstance(ans, list) else [ans]
    elif isinstance(selector, ElementBase):
        return [selector]

    nodes = node.cssselect(selector)
    if node in nodes:
        nodes.remove(node)

    return nodes


def _fake_node(d, ds):
    node = uuid4()
    ds[node] = d
    return node


class Group(object):
    """Contains nodes, and a pointer
    to the parentNode for this group"""
    def __init__(self, parent, nodes=None):
        self.parentNode = parent
        self.nodes = nodes if nodes is not None else list()

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
    """A container of groups"""

    def __init__(self, root):
        self.groups = []
        self.dataset = root.dataset
        self.root = root

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

    def __init__(self, root):
        super(EnterSelection, self).__init__(root)

    def select(self, selector):
        sel = Selection(self.root)
        ds = self.dataset

        for group in self:
            update = group.updates
            subgroup = Group(group.parentNode)
            sel.append(subgroup)
            for i, node in enumerate(group):
                if node is not None:
                    data = ds.get(node, None)

                    subnode = _select(group.parentNode, selector, data, i)
                    subgroup.append(subnode)

                    if subnode is not None:
                        ds[subnode] = data

                    update[i] = subnode
                else:
                    subgroup.append(None)

        return sel


class Selection(BaseSelection):

    def __init__(self, root):
        super(Selection, self).__init__(root)

    def selectAll(self, selector):
        sel = Selection(self.root)
        ds = self.dataset

        for group in self:
            for node in group:
                if node is not None:
                    sel.append(Group(
                        node,
                        _selectAll(node, selector, ds.get(node, None))
                    ))

        return sel

    def select(self, selector):
        sel = Selection(self.root)

        for group in self:
            subgroup = Group(group.parentNode)
            sel.append(subgroup)
            for i, node in enumerate(group):
                if node is not None:
                    data = self.dataset.get(node, None)

                    subnode = _select(node, selector, data, i)
                    subgroup.append(subnode)

                    if subnode is not None:
                        self.dataset[subnode] = data
                else:
                    subgroup.append(None)

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

    def attr(self, name, val=None):

        if val is None:
            return self.node().get(name, None)

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
                    enters[i] = _fake_node(node_data, self.dataset)

            for i in range(n0, m):
                enters[i] = _fake_node(data[i], self.dataset)

            for i in range(m, n):
                exits[i] = group[i]

            exit.append(Group(group.parentNode, exits))

            ugroup = Group(group.parentNode, updates)
            egroup = Group(group.parentNode, enters)
            egroup.updates = ugroup

            update.append(ugroup)
            enter.append(egroup)
            enter.update = update

        enter = EnterSelection(self.root)
        update = Selection(self.root)
        exit = Selection(self.root)

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

    def html(self):
        return tostring(self.document, pretty_print=True, doctype='<!doctype html>')

    def select(self, selector):
        sel = Selection(self)
        subgroup = Group(self.document)
        subgroup.append(_select(self.document, selector))
        sel.append(subgroup)
        return sel

    def selectAll(self, selector):
        sel = Selection(self)
        subgroup = Group(self.document)
        subgroup.append(_selectAll(self.document, selector))
        sel.append(subgroup)
        return sel
