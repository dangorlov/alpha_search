
def GetAll(city='Moscow'):
    key = "8145067c7165efd3c8450482714282c7"
    import requests
    result = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&appid=8145067c7165efd3c8450482714282c7'.format(city)).json()
    temp = int(result['main']['temp'])-273,15
    w_descr = result['weather'][0]['description']
    return {'temp':temp, 'w_dscr':w_descr, 'm_json':result}
    #return result


print(GetAll('Moscow'))