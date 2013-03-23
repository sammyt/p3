from p3 import P3
from pyvows import Vows, expect

from lxml.html import builder as E
from lxml.html import fromstring, tostring


@Vows.batch
class SelectionFilter(Vows.Context):

    class SelectAllDiv(Vows.Context):
        """select_all(div)"""

        def topic(self):
            p3 = P3(E.HTML(E.HEAD(), E.BODY()))
            div = p3.select('body').select_all('div').data([0,1])

            nest = div.enter().create('div').select_all('span')

            def _manip(node, d, i):
                d = d << 1
                return [d, d + 1]

            return nest.data(_manip).enter().create('span')

        def preserves_matching_elements(self, span):
            some = span.filter(lambda n, d, i: i == 0)
            expect(some[0][0]).to_equal(span[0][0])

        def removes_non_matching_elements(self, span):
            some = span.filter(lambda n, d, i: bool(d & 1))
            some = [item for sublist in some for item in sublist]

            expect(some).Not.to_include(span[0][0])
            expect(some).Not.to_include(span[1][0])

        def preserves_data(self, span):
            some = span.filter(lambda n, d, i: bool(d & 1))
            ds = some.root.dataset
            expect(ds.get(some[0][0])).to_equal(1)
            expect(ds.get(some[1][0])).to_equal(3)

        def preserves_grouping(self, span):
            some = span.filter(lambda n, d, i: bool(d & 1))
            expect(some).to_length(2)
            expect(some[0]).to_length(1)
            expect(some[1]).to_length(1)

        def can_be_a_css_selector(self, span):
            span[0][0].attrib["class"] = "foo"
            some = span.filter('.foo')
            expect(some).to_length(2)
            expect(some[0]).to_length(1)
            expect(some[1]).to_length(0)







