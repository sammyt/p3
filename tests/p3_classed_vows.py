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
                E.BODY(
                    E.DIV()
                )
            )
            return P3(html).select('body')

        def add_missing_class_when_true(self, body):
            node = body.node()
            body.classed('foo', True)
            expect(node.attrib['class']).to_equal('foo')

        def removes_existing_when_false(self, body):
            node = body.node()
            body.classed('foo', True)
            expect(node.attrib['class']).to_equal('foo')
            body.classed('foo', False)
            expect(node.attrib).Not.to_include('class')

        def preserves_existing_class(self, body):
            node = body.node()
            body.classed('foo', True)
            body.classed('foo', True)
            expect(node.attrib['class']).to_equal('foo')

        def preserves_missing_class(self, body):
            node = body.select('div').node()
            sel = body.select('div')
            sel.classed('boo', True)
            sel.classed('foo', False)
            sel.classed('foo', False)
            expect(node.attrib['class']).to_equal('boo')

        def can_use_callable_as_value(self, body):
            sel = body.create('span')
            node = sel.node()

            sel.classed('baar', lambda n, d, i: True)
            expect(node.attrib['class']).to_equal('baar') 








        