from flask import Flask,url_for,render_template,session,g,redirect,abort,flash
from flask import request,make_response
import os
import sqlite3
import pymysql


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

##DB
#mysql
#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1', charset='utf8')




##DB
#connect DB
def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory=sqlite3.Row
    return rv

#get DB
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

#init DB
def init_db():
    db=get_db()
    with app.open_resource('schema.sql','r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

##show entrites
@app.route('/showen/')
def show_entries():
    db=get_db()
    cur=db.execute('select title, text from entries order by id desc')
    entries=cur.fetchall()
    return render_template('show_entries.html',entries=entries)

##add entrites
@app.route('/adden/',methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db=get_db()
    db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'],request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

##login
@app.route('/login/',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME']:
            error='Invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error='Invalid password'
        else:
            session['logged_in']=True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

##logout
@app.route('/logout/')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

##router
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello_world(name):
    return render_template('hello.html',name=name)

## R/W cookies
@app.route('/wck/<username>/')
def write_cookies(username):
    resp=make_response(render_template('index.html'))
    resp.set_cookie('username',username)
    return resp

@app.route('/rck/')
def read_cookies():
    username=request.cookies.get('username')
    return username

##构造url
with app.test_request_context():
 url_for('static',filename='style.css')

###file upload
@app.route('/upload/',methods=['GET','POST'])
def upload_file():
    if request.method=='GET':
        return render_template('upload.html')
    if request.method=='POST':
        f=request.files['the_file']
        f.save('/Users/xuzhengxi/PycharmProjects/flask-web/upload/upload_file.txt')
        return 'upload success.'



if __name__ == '__main__':
    app.debug=True
    app.run()
