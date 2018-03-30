from flask import *
from indexer import indexing
from indexer import build_index, dict_optimization
from indexer.search_engine import *
from spider import spider
from config import *
import json

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


def op(fp):
    with open(fp, 'r', encoding='cp1251') as fl:
        return fl.read()


def query_search(req):
    print(req[:-1])
    query_string = query_stack.process(req)
    results = query_string.get_query_urls(len(url_list))

    print(len(results))
    for doc_url_idx in results:
        print(url_list[doc_url_idx])


if __name__ == '__main__':
    # spider.run()
    # app.run(HTTP_IP, port=HTTP_PORT)

    # Build index
    with open('index.json') as f:
        index = json.load(f)
    files = [(int(i), {'url': url, 'text': op('root/' + i + '.txt')}) for i, url in zip(index, index.values())]
    indexing.run('simple9', files)
    build_index.run()
    dict_optimization.run()

    # Search engine
    path = './temp_idx/'
    with open(path + 'encoding.ini', 'r') as f_config:
        encoding = f_config.readline()
    index = SearchIndex(path + 'entire_index', path + 'terms_dict', encoding)
    with open(path + 'url_list', 'r') as urls_filename:
        url_list = urls_filename.readlines()
        url_list = [url[:-1] for url in url_list]
    query_stack = QueryProcessor(index)

    query_search('test')
