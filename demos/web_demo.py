from p3 import P3
from lxml.html import tostring
from flask import Flask

app = Flask("p3-demo")
app.debug = True


def head(selection):
    selection.create('meta').attr('charset', 'utf-8')
    selection.create('style').attr('href', 'styles.css').attr('rel', 'stylesheets')


def heading(selection):
    selection.create('h1').text('Building With P3')


def footer(selection):
    selection.create('p').text('we all need a footer')


def content(selection):
    selection.create('div').classed('slow', True).call(slow_content)
    selection.create('div').classed('lastest', True).call(lastest_news)


def slow_content(selection):
    selection.text("""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex""")



def lastest_news(selection):
    news = [
        'barnacles storm building',
        'code all the things!',
        'pond floods cabbage patch'
    ]
    ol = selection.create('ol')
    update = ol.select_all('li').data(news)
    update.enter().create('li')
    update.text(lambda n, d, i: d)


@app.route("/")
def index():
    p3 = P3()

    # update the <head/>
    p3.select('head').call(head)

    # select the <body/>
    body = p3.select('body')

    # render the page sections
    body.create('header').call(heading)
    body.create('section').call(content)
    body.create('footer').call(footer)

    return tostring(p3.document)

if __name__ == "__main__":
    app.run()
