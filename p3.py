import lxml
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector

html = E.HTML(
    E.HEAD(),
    E.BODY()
)


class Selection(object):

    def __init__(self, items):
        super(Selection, self).__init__()
        self.items = items

    def select(self, selector):
        node = self.items[0]
        return Selection([node.cssselect(selector)[0]])

    def selectAll(self, selector):
        next = []
        for node in self.items:
            next += node.cssselect(selector)

        return Selection(next)

    def append(self, tag):
        for node in self.items:
            node.append(fromstring('<' + tag + "/>"))
        return self


class P3(object):

    def __init__(self):
        super(P3, self).__init__()

    def select(self, ctx):
        return Selection([html]).select(ctx)

    def selectAll(self, ctx):
        return Selection([html]).selectAll(ctx)

p3 = P3()


def main():

    p3.select("body").append("div")
    p3.select("body").append("div")

    p3.select("body").select("div").append("p")
    p3.select("body").selectAll("div").append("span")

    print lxml.etree.tostring(html, pretty_print=True)


if __name__ == '__main__':
    main()
