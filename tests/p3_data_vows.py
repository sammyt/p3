from p3 import P3
from pyvows import Vows, expect

import lxml
from lxml.etree import ElementBase
from lxml.html import builder as E
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector


@Vows.batch
class SelectionData(Vows.Context):

    class SelectBody(Vows.Context):
        """select(body)"""

        def topic(self):
            html = E.HTML(E.HEAD(), E.BODY())
            return P3(html).select('body')

        def assign_data_as_a_list(self, body):
            data = 'foo'
            body.data([data])

            ds = body.root.dataset
            expect(ds[body[0][0]]).to_equal(data)

        def assign_data_as_a_callable(self, body):
            data = 'foo'
            body.data(lambda g, d, i: [data])
            ds = body.root.dataset

            expect(ds[body[0][0]]).to_equal(data)

        def with_no_arguments_returns_list(self, body):
            body.data(['foo'])
            expect(body.data()).to_equal(['foo'])

    class SelectAllDiv(Vows.Context):
        """select_all(div)"""

        def topic(self):
            p3 = P3(E.HTML(E.HEAD(), E.BODY()))
            div = p3.select('body').select_all('div')
            return div.data(range(2)).enter().create("div")
