from flask import Flask, request, redirect, session, Markup, render_template, flash, Markup
import os


app = Flask(__name__, template_folder='templates')


app.secret_key=os.environ["SECRET_KEY"];


@app.route("/")
def render_main():
    print("RunningMain")
    return render_template('page1.html')
@app.route('/login/authorized')
   def login():
      return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))
@app.route('/startOver')
def startOver():
    session.clear() 
    return redirect('/page1')
@app.route('/page1',methods=['GET','POST'])
def renderPage1():
    return render_template('page1.html')
@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    session["firstName"]=request.form['firstName']
    session["lastName"]=request.form['lastName']
    return render_template('page2.html')

  
if __name__ == "__main__":
    app.run(debug=True)
