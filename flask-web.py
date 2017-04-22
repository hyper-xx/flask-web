from flask import Flask,url_for,render_template
from flask import request,make_response

app = Flask(__name__)

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
