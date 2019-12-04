from flask import *
import jwt
import time

app = Flask(__name__)
priv_key = open("5da000144cdbfb621b13e35c399f3782", "br").read(10000)
pub_key = open("181172d482b851b0cebdf777eabcb007.pub", "br").read(10000)

def make_token(username):
	data = {'user': username, 'iat': int(time.mktime(time.localtime()))}
	token = jwt.encode(data, priv_key, 'RS256')
	return token

def check_token(request):
	if 'token' not in request.cookies:
		return False
	token = request.cookies.get('token')
	try:
		data = jwt.decode(token, pub_key)
		if data['user'] != 'admin':
			return False
	except:
		return False
	return True

@app.route("/")
def index():
	resp = make_response(render_template('index.html'))	
	if 'token' not in request.cookies:
		resp.set_cookie('token', make_token('guest'))
	return resp

@app.route("/flag")
def flag():
	if check_token(request):
		return render_template('flag.html')
	else:
		return render_template('not_flag.html', token=request.cookies.get('token'))

@app.route("/5da000144cdbfb621b13e35c399f3782")
def private():
	return render_template('priv_key.html')

@app.route("/181172d482b851b0cebdf777eabcb007.pub")
def public():
	return render_template('pub_key.html', pub_key=str(pub_key))

if __name__ == "__main__":
    app.run(port=80)
