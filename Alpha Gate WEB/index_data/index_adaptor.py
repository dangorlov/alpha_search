def Find(query=' '):
    '''

    :param query: string, which describes a query
    :return: results: list like [["name", 'url', 'description']]
    '''
    query = query.replace(" ", "&")
    results = [["Задан пуской поисковый запрос.", '/', 'Эй ты! Чего запросы писать забываем?']]
    #for i in results:
    #    i[2]="<div>{0}</div>".format(i[2])
    return results