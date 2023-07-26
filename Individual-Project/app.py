from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config = {
  'apiKey': "AIzaSyAV8PUpTgePu9ki-HDZZbvOz8c6sZoNlbk",
  'authDomain': "spotify-8be88.firebaseapp.com",
  'projectId': "spotify-8be88",
  'storageBucket': "spotify-8be88.appspot.com",
  'messagingSenderId': "594905802853",
  'appId': "1:594905802853:web:6dba497a68e103b24f7e8c",
  "databaseURL":"https://spotify-8be88-default-rtdb.europe-west1.firebasedatabase.app/"
}

#Code goes below here

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
@app.route('/')
def  home():
    return render_template('index.html')

@app.route("/main")
def main():
    return render_template('main.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error= ""
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('main'))
        except:
            error = 'signin failed'
            return render_template("signin.html")
    else:
        return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error= ""
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']

        # try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)

        UID = login_session['user']['localId']
        user = {"email":email,"password":password,"full_name":full_name,"username": username }
        db.child("Users").child(UID).set(user)
        return redirect(url_for('signin'))
        # except:
        #      error = "auth failed"
        #      return render_template("signup.html")
    else:
        return render_template('signup.html')


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)