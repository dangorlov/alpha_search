from flask import Flask, request, make_response, render_template, send_from_directory, redirect, abort
import uuid



admin = ('admin', '12345678')
idw = str(uuid.uuid4())
try:
    import index_data.index_adaptor
except:
    print('SearchEngine import failed. Only demo functionality')
app = Flask(__name__, template_folder='templates')


def WriteData(pth, request):
    f = open('click_stat.dat', 'a')
    f.write("{0}\t{1}\n".format(request, pth))
    f.close()


page_rank = {}


@app.route('/<path:pth>')
def MainTemplateHandler(pth):
    try:
        return render_template(pth)
    except:
        abort(404)


@app.route('/')
def index():
    import geoip
    ips = request.remote_addr
    print(ips)
    loc = str(request.accept_languages).split(",")[0]
    a = geoip.open_database(
        'service_data/geoip_data.mmdb')  # ip='8.8.8.8' country='US' continent='NA' subdivisions=frozenset() timezone='None' location=(37.751, -97.822)
    print(a.lookup(ips))
    return (render_template('alpha_gate.html', loc=loc))


@app.route('/gsearch')
def index_o():
    loc = str(request.accept_languages).split(",")[0]
    if loc == "ru":
        f = open("ru_exmp.txt", encoding='utf-8')
        exmp = f.read()
        f.close()
    else:
        f = open("en_exmp.txt")
        exmp = f.read()
        f.close()
    return (render_template('index.html', loc=loc, exmp=exmp))


@app.route('/redirect/<string:rname>/<path:pth>')
def redir(rname, pth):
    WriteData(pth, rname)
    return redirect(pth, code=302)


@app.route('/flask_api/login')
def auth():
    password = request.args.get('password')
    login = request.args.get('email')
    if login == admin[0] and password == admin[1]:
        resp = make_response(redirect('/admin_panel/panel.html', code='302'))
        resp.set_cookie('userID', idw)
        return resp
    else:
        return redirect('/admin_panel/login.html')


@app.route('/admin_panel/panel.html')
def panel():
    try:
        uid = request.cookies.get('userID')
        if uid == idw:
            return render_template('admin_panel/panel.html')
        else:
            abort(403)
    except:
        return redirect("/admin_panel/login.html")


@app.route('/admin_functional/s_kill')
def panesl():
    try:
        uid = request.cookies.get('userID')
        print(uid)
        if uid == idw:
            return "Sorry! But is temporarily not avable"
        else:
            abort(403)
    except:
        return redirect("/admin_panel/login.html")


@app.route('/static/<path:pth>')
def statics(pth):
    return send_from_directory(directory='static', path=pth)


@app.route('/flask_api/search')
def get_search():
    res = index_data.index_adaptor.Find(request.args.get('s'))
    for i in range(len(res)):
        res[i][1] = "/redirect/{0}/{1}".format(request.args.get('s'), res[i][1])
    return render_template(
        'search_jinja.html',
        results=res,
        t_num=len(res),
        r_name=request.args.get('s')
    )


@app.route('/weather')
def weather():
    def capitalize(string, lower_rest=False):
        return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])

    import weather_utils, geoip
    ips = request.remote_addr
    m_data = weather_utils.GetAll(ips=ips, city="Puschino")
    temp = m_data['temp'][0]
    status = m_data['w_dscr']
    print("Temp:", temp, "Status:", status)
    if status == 'clear sky':
        status_img = 'clear_sky.jpg'
    return render_template('weather.html', temp=temp, status=capitalize(status), status_img=status_img)


import webbrowser

# webbrowser.open("http://127.0.0.1:8081/")
app.run(host="0.0.0.0", port=8081)
