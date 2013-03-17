from p3 import P3
from pyvows import Vows, expect

import lxml

from lxml.etree import ElementBase
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector


@Vows.batch
class SelectionSelectAll(Vows.Context):

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

        def select_all_matching(self, body):
            div = body.selectAll('div')
            doc = div.root.document

            expect(div[0][0]).to_equal(doc[1][0])
            expect(div[0][1]).to_equal(doc[1][1])

        def progrates_parent_to_selected(self, body):
            div = body.selectAll('div')
            doc = div.root.document

            expect(div[0].parentNode).to_equal(doc[1])

        def does_not_propogate_data(self, body):
            div = body.data(['a', 'b']).selectAll('div')
            ds = div.root.dataset

            expect(ds.get(div[0][0], "nope")).to_equal('nope')
            expect(ds.get(div[0][1], "nope")).to_equal('nope')

        def returns_an_empty_array_if_no_match(self, body):
            span = body.selectAll('span')
            expect(span).to_length(1)
            expect(span[0]).to_length(0)

        def can_select_by_function(self, body):
            data = 'foo'
            datas = []
            indexes = []
            nodes = []
            doc = body.root.document
            doc_body = doc[1]

            def to_call(node, data, index):
                print node, data, index
                datas.append(data)
                indexes.append(index)
                nodes.append(node)
                return node.getchildren()

            s = body.data([data]).selectAll(to_call)

            expect(datas).to_equal([data])
            expect(indexes).to_equal([0])
            expect(nodes).to_equal([doc_body])

            expect(s[0][0]).to_equal(doc_body[0])
            expect(s[0][1]).to_equal(doc_body[1])



    class SelectAllDiv(Vows.Context):
        """selectAll(div)"""

        def topic(self):
            html = E.HTML(
                E.HEAD(),
                E.BODY()
            )
            p3 = P3(html)
            div = p3.select('body').selectAll('div')\
              .data(range(2)).enter().create("div")

            div.create("span").attr("class", "first")
            div.create("span").attr("class", "second")
            return div

        def select_all_mathching(self, div):
            span = div.selectAll('span')
            expect(span).to_length(2)
            expect(span[0]).to_length(2)

            expect(span[0][0].getparent()).to_equal(div[0][0])
            expect(span[0][1].getparent()).to_equal(div[0][0])
            expect(span[1][0].getparent()).to_equal(div[0][1])
            expect(span[1][1].getparent()).to_equal(div[0][1])

        def propogates_parent_to_selected(self, div):
            body = div.root.document[1]
            span = div.selectAll('span')
            expect(span[0].parentNode).to_equal(body[0])
            expect(span[1].parentNode).to_equal(body[1])


        def returns_an_empty_array_if_no_match(self, div):
            sub = div.selectAll('div')
            expect(sub).to_length(2)
            expect(sub[0]).to_length(0)
            expect(sub[1]).to_length(0)












        