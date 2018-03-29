from flask import Flask, request, render_template, send_from_directory, redirect, abort
try:
  import index_data.index_adaptor
except: print('SearchEngine import failed. Only demo functionality')
app = Flask(__name__,template_folder='templates')

def WriteData(pth, request):
    f = open('page_rang.dat', 'a')
    f.write("{0}\t{1}\n".format(request, pth))
    f.close()
page_rank={}

@app.route('/<path:pth>')
def MainTemplateHandler(pth):
    try:
      return render_template(pth)
    except:
      abort(404)
@app.route('/')
def index():
    return(render_template('alpha_gate.html'))
@app.route('/gsearch')
def index_o():
    return(render_template('index.html'))
@app.route('/redirect/<string:rname>/<path:pth>')
def redir(rname, pth):
    WriteData(pth, rname)
    return redirect(pth, code=301)


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
    import weather_utils
    m_data = weather_utils.GetAll()
    temp = m_data['temp'][0]
    status = m_data['w_dscr']
    print("Temp:",temp, "Status:",status)
    if status == 'clear sky':
        status_img='clear_sky.jpg'
    return render_template('weather.html', temp=temp, status=status, status_img=status_img)

import webbrowser
webbrowser.open("http://127.0.0.1:8081/")
app.run(host="0.0.0.0",port=8081)
