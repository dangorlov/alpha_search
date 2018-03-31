from flask import *
from indexer import indexing
from indexer import build_index, dict_optimization
from indexer.search_engine import *
from indexer import doc2words
from config import *
import random

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def index():
    return redirect(url_for('alpha_se'))


@app.route('/gsearch')
def alpha_se():
    examples = [i for i in doc2words.dct]
    if len(examples):
        ex = random.choice(examples)
    else:
        ex = 'Поиск...'
    return render_template('main.html', exmp=ex)


@app.route('/search')
def search():
    req = request.args.get('req')
    if req is None:
        abort(418)
    res = []
    for r in req.split():
        try:
            for url in query_search(r):
                snippet = indexing.get_snippet(url, doc2words.normal(req))
                res.append({'url': url_list[url], 'head': snippet[0], 'body': snippet[1]})
        except:
            pass
    return render_template('search.html',
                           request=req,
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
    req = doc2words.normal(req)
    query_string = query_stack.process(req)
    results = query_string.get_query_urls(len(url_list))

    for doc_url_idx in results:
        yield doc_url_idx


def generate_index(ind):
    print('Генерация индекса...')
    files = [(int(i), {'url': url, 'text': op('root/' + str(i) + '.txt')}) for i, url in zip(ind, ind.values())]
    indexing.run('simple9', files)
    build_index.run()
    dict_optimization.run()


if __name__ == '__main__':
    from spider.spider import CrawlerRunner
    CrawlerRunner()

    # Search engine
    path = './temp_idx/'
    with open(path + 'encoding.ini', 'r') as f_config:
        encoding = f_config.readline()
    index = SearchIndex(path + 'entire_index', path + 'terms_dict', encoding)
    with open(path + 'url_list', 'r') as urls_filename:
        url_list = urls_filename.readlines()
        url_list = [url[:-1] for url in url_list]
    query_stack = QueryProcessor(index)

    # print(indexing.get_snippet(list(query_search('Британецы'))[0], doc2words.normal('Британецы')))
    app.run(HTTP_IP, port=HTTP_PORT)
