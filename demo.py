
def main():
    import lxml
    from lxml.html import builder as E
    from lxml.cssselect import CSSSelector

    from p3 import P3

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
        return "data:%s index:%s" % tuple([d, i])

    sel = p3.select("body").selectAll("div").selectAll("p")

    sel = sel.data(['a', 'b', 'c', 'd', 'e'])

    for group in sel.enter():
        print list(group)
    
    sel.enter().create('p')    
    sel.text(echo)

    #sel.data(['a', 'b']).exit().text("gone")
    
    print(lxml.etree.tostring(html, pretty_print=True))

    print p3.select('body').select('div')

if __name__ == '__main__':
    main()
