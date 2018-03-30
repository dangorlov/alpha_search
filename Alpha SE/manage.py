from flask import *
from indexer import indexing
from spider import spider
from config import *

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/search')
def search():
    res = [
        {
            'url': url_for('go', url='https://mail.ru'),
            'head': 'Mail.ru',
            'body': 'some text'
        }
    ]
    return render_template('search.html',
                           request=request.args.get('req'),
                           num=len(res),
                           results=res)


@app.route('/go')
def go():
    # Do something
    return redirect(request.args.get('url'), code=301)


if __name__ == '__main__':
    spider.run()
    # app.run(HTTP_IP, port=HTTP_PORT)
    # indexing.run('simple9', 'data/lenta.ru_4deb864d-3c46-45e6-85f4-a7ff7544a3fb_01.gz')
    pass
