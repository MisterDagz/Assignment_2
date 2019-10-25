from flask import Flask, request, render_template


app=Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

users = {}

@app.route('/')
def home():
	return render_template('base.html', title="Home")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		# .get returns none if form value not there
		uname = request.form.get("uname")
		pword = request.form.get('pword')
		twofa = request.form.get('2fa')
		if uname in users:
			return render_template('register.html', title="Register", message="""Failure: User already Exists""")
		else:
			jblob = {"username": uname, "password": pword, "2fa": twofa}
			users[uname] = jblob
			return render_template('register.html', title="Register", message="""Success: Account Created""")
			
	if request.method == 'GET':
		return render_template('register.html', title="Register")
	
@app.route('/login')
def login():
	return "Blank"
@app.route('/spell_check')
def spell_check():
	return "Blank"
if __name__=="__main__":
	app.run()
