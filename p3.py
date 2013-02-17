import lxml
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector

html = E.HTML(
    E.HEAD(),
    E.BODY()
)
    

def string_selector(sel):
    return lambda n, d, i, j: n.cssselect(sel)

def _selector(s):
    if isinstance(s, str):
        return string_selector(s)
    return s


class Selection(object):

    def __init__(self, items):
        super(Selection, self).__init__()
        self.items = items

    def select(self, s):
        node = self.items[0][0]
        return Selection([_selector(s)(node, None, 0, 0)[:1]])

    def selectAll(self, s):
        next = []
        for j, sel in enumerate(self.items):
            for i, node in enumerate(sel):
                next.append(_selector(s)(node, None, i, j))

        return Selection(next)

    def append(self, tag):
        next = []
        for node in self.items:
            n = fromstring('<' + tag + "/>")
            next.append(n)
            node.append(n)
        return Selection(next)

    def text(self, copy):
        if isinstance(copy, str):
            for node in self.items:
                node.text = copy
        elif hasattr(copy, '__call__'):
            for i, node in enumerate(self.items):
                node.text = copy(None, i, None)


class P3(object):

    def __init__(self):
        super(P3, self).__init__()

    def select(self, ctx):
        return Selection([[html]]).select(ctx)

    def selectAll(self, ctx):
        return Selection([[html]]).selectAll(ctx)

p3 = P3()


def main():

    p3.select("body").append("div")
    p3.select("body").append("div")

    p3.select("body").select("div").append("p")
    p3.select("body").selectAll("div").append("span").text("hi")

    p3.select("body").selectAll("div").selectAll("span").text(lambda d, i, j: "woo %s" % i)

    print lxml.etree.tostring(html, pretty_print=True)


if __name__ == '__main__':
    main()
