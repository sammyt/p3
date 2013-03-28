from p3 import P3
from pyvows import Vows, expect
from lxml.html import builder as E


@Vows.batch
class SelectionClassed(Vows.Context):

    class SelectBody(Vows.Context):
        """select(body)"""

        def topic(self):
            html = E.HTML(
                E.HEAD(),
                E.BODY()
            )
            return P3(html).select('body')


        def sets_the_innerHTML_as_a_string(self, body):
            div = body.create('div').html('<span>omg</span')
            node = div.node()[0]
            expect(node.tag).to_equal('span')
            expect(node.text).to_equal('omg')


        def sets_the_innerHTML_with_callable(self, body):
            div = body.create('div').html(lambda n, d, i : '<strong>wooo</strong>')
            node = div.node()[0]
            expect(node.tag).to_equal('strong')
            expect(node.text).to_equal('wooo')

        def empty_string_clears_contents(self, body):
            sel = body.create('div')
            sel.create('span').text('hello')
            sel.html('')
            expect(sel.node().getchildren()).to_length(0)
