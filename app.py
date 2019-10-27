from flask import Flask, request, render_template, make_response, redirect, session
import random
import string
import subprocess
app=Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

users = {}
cookies = {}
def randomString(stringLength=20):
	letters = string.ascii_lowercase
	letters += "0123456789"

	return ''.join(random.choice(letters) for i in range(stringLength))

def checkcookie(auth, userid):
	#enforces an allowed number of failures for cookie auth, if it exceeds 3, the current cookie for the user is invalid.
	if auth in cookies.keys():
		if cookies[auth]['username'] == userid:
			return True
		else:
			cookies[auth]['failurecount'] += 1
		if cookies[auth]['failurecount'] >=3:
			cookies.pop(auth, None)
	
	if userid in users:
		cookie = users[userid].get('cookie', None)
		if cookie is not None:
			cookies[cookie]['failurecount'] +=1 
			if cookies[auth]['failurecount'] >=3:
				cookies.pop(auth, None)
	return False

@app.route('/')
def home():
	return render_template('base.html', title="Home")

@app.route('/register', methods=['GET', 'POST'])
def register():
	
	#if request.method == 'POST':
		# .get returns none if form value not there
	uname = request.form.get("uname")
	pword = request.form.get('pword')
	twofa = request.form.get('2fa')
	
	if uname is not None:
		if uname in users:
			return render_template('register.html', title="Register", message="""failure""")
		
		else:
			jblob = {"username": uname, "password": pword, "2fa": twofa}
			users[uname] = jblob
			
			return render_template('register.html', title="Register", message="""success""")
			
	#if request.method == 'GET':
	else:
		return render_template('register.html', title="Register")
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	uname = request.form.get("uname")
	pword = request.form.get('pword')
	twofa = request.form.get('2fa')
	
	if uname is not None :
		# .get returns none if form value not there

		if uname not in users:
			return render_template('login.html', title="Login", message="""Incorrect Username or Password""")
		else:
			if pword != users[uname]["password"]:
				return render_template('login.html', title="Login", message="""Incorrect Username or Password""")
			elif twofa != users[uname]["2fa"]:
				return render_template('login.html', title="Login", message="""Two-factor Authentication Failure, wrong code supplied""")
			else:
				resp = make_response(render_template('login.html', title="Register", message="""Success"""))
				auth_token = randomString(20)
				# Failure count is to check if someone is trying to enumerate the cookie for a user
				cookies[auth_token] = {'username':uname, 'failurecount':0}
				users[uname]['cookie'] = auth_token
				session['auth'] = auth_token
				session['username'] = uname
				return resp
			
	else:
		"""
		if request.cookies.get('auth') is not None:
			auth = request.cookies.get('auth')
			if auth in cookies.keys():
				if checkcookie(auth, cookies[auth]['username']):
					return redirect("/")
		"""
		return render_template('login.html', title="Login")
	
@app.route('/spell_check', methods=["GET", "POST"])
def spell_check():	
	
	authorized = False

	if 'auth' in session.keys():
		if session['auth'] is not None:
			auth = session['auth']
			if auth in cookies.keys():	
				uname = session['username']
				if uname is not None:
					if checkcookie(auth, uname):
						authorized = True
					else:
						return redirect("/")
				else:
					return redirect("/")
			else:
				return redirect("/")
		else:
			return redirect("/")
	else:
		return redirect("/")


	if authorized:
		
		if request.method == 'GET':
			return render_template('spell_check.html', title="Spell Check")
		if request.method == 'POST':
			text = request.form.get('inputtext')
			if text is None:
				text = ""
			f = open("test.txt", "w")
			f.write(text)
			f.close()
			MyOut = subprocess.Popen(['./a.out', 'test.txt', 'wordlist.txt'], stdout=subprocess.PIPE)
			
			stdout,stderr = MyOut.communicate()
			miss = stdout.decode('utf-8')
			miss = miss.replace('\n',',')
			if miss[len(miss)-1] ==",":
				miss = miss[:len(miss)-1]
			
			return render_template('spell_check.html', title="Spell Check", textout=text, misspelled=miss)


if __name__=="__main__":
	app.run()
