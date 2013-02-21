import lxml
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
 


class Selection(list):

    @classmethod
    def create(cls, node):
        sel = Selection()
        sel.append(node)
        sel.parentNode = node
        root = Selection()
        root.append(sel)
        return root

    def each(fn):
        def wrapped(self, *args):
            for group in self:
                for node in group:
                    if node is not None: 
                        fn(self, node, *args)
            return self
        return wrapped

    @each
    def text(self, node, text):
        node.text = text
        

    def select(self, selector):
        sel = Selection()

        for m, n in enumerate(self):
            sub = Selection()
            group = self[m]
            sel.append(sub)
            sub.parentNode = group.parentNode
            for i, node in enumerate(group):
                if node is not None:
                    found = node.cssselect(selector)[0]
                    sub.append(found)


        return sel



def select(context):
    return Selection.create(context)


def selectAll(selector):
    pass


def main():
    print select(html).select("body")
    print select(html).select("body").select(".foo")
    print select(html).select("body").select(".foo").text("hi")
    
    print lxml.etree.tostring(html, pretty_print=True)


if __name__ == '__main__':
    main()
