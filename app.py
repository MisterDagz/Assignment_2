from flask import Flask, request

app=Flask(__name__)

users = {}
@app.route('/')
def home():
	return "<h1> Hello World 2</h1>"

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		# .get returns none if form value not there
		uname = request.form.get("uname")
		pword = request.form.get('pword')
		twofa = request.form.get('2fa')
		if uname in users:
			return """failure: User already Exists"""
		else:
			jblob = {"username": uname, "password": pword, "2fa": twofa}
			users[uname] = jblob
			
	if request.method == 'GET':
		pass
	
@app.route('/login')
	def login():
		pass
@app.route('/spell_check')
	def spell_check():
		pass
if __name__=="__main__":
	app.run()
