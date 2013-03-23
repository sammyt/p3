from p3 import P3
from pyvows import Vows, expect

import lxml

from lxml.etree import ElementBase
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector


@Vows.batch
class SelectionSelect(Vows.Context):

    class SelectBody(Vows.Context):
        """select(body)"""

        def topic(self):
            html = E.HTML(
                E.HEAD(),
                E.BODY(
                    E.DIV(E.CLASS('first')),
                    E.DIV(E.CLASS('second')))
            )
            return P3(html).select('body')

        def select_first_match(self, body):
            div = body.select('div')
            node = div.root.document.cssselect('.first')[0]
            expect(div[0][0]).to_equal(node)

        def propagates_parent_node_to_selected(self, body):
            div = body.select('div')
            group = div[0]
            expect(group.parent_node).to_equal(body.root.document)

        def propogates_data_to_selected(self, body):
            data = {}
            div = body.data([data]).select('div')
            expect(div.data()[0]).to_equal(data)

        def returns_none_when_no_match(self, body):
            span = body.select('span')
            expect(span[0][0]).to_equal(None)
            expect(len(span)).to_equal(1)
            expect(len(span[0])).to_equal(1)

        def can_select_by_callable(self, body):
            data = {}
            datas = []
            indexes = []
            nodes = []
            doc = body.root.document

            def to_call(node, data, index):
                datas.append(data)
                indexes.append(index)
                nodes.append(node)

            body.data([data]).select(to_call)

            expect(datas).to_equal([data])
            expect(indexes).to_equal([0])
            expect(nodes).to_equal([doc.cssselect('body')[0]])


    class SelectAllDiv(Vows.Context):
        """select_all(div)"""

        def topic(self):
            html = E.HTML(
                E.HEAD(),
                E.BODY()
            )
            p3 = P3(html)
            div = p3.select('body').select_all('div')\
              .data(range(2)).enter().create("div")

            div.create("span").attr("class", "first")
            div.create("span").attr("class", "second")
            return div

        def select_first_match(self, div):
            span = div.select('span')

            expect(span[0][0].getparent()).to_equal(div[0][0])
            expect(span[0][1].getparent()).to_equal(div[0][1])
            
            expect(span).to_length(1)
            expect(span[0]).to_length(2)
            expect(span.attr('class')).to_equal('first')

        def propogate_parent_node_to_selected(self, div):
            span = div.select('span')
            body = div.root.document[1]
            expect(span[0].parent_node).to_equal(body)
            expect(span[0].parent_node).to_equal(div[0].parent_node)

        def propogates_data_to_selected(self, div):
            data = {}
            span = div.data([data]).select('span')
            expect(span.data()[0]).to_equal(data)

        def returns_none_when_no_match(self, div):
            sub = div.select('div')
            expect(sub[0][0]).to_equal(None)
            expect(sub[0][1]).to_equal(None)
            expect(sub).to_length(1)

        
        def can_select_by_callable(self, div):
            d = ["a", "b"]
            datas = []
            indexes = []
            nodes = []
            doc = div.root.document

            def to_call(node, data, index):
                datas.append(data)
                indexes.append(index)
                nodes.append(node)
                return node[0]

            s = div.data(d).select(to_call)

            expect(datas).to_equal(["a", "b"])
            expect(indexes).to_equal([0, 1])
            expect(nodes[0]).to_equal(div[0][0])
            expect(nodes[1]).to_equal(div[0][1])
            expect(s[0][0]).to_equal(div[0][0][0])
            expect(s[0][1]).to_equal(div[0][1][0])
            












