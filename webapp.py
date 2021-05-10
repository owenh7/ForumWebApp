from flask import Flask, request, redirect, session, Markup, render_template, flash, Markup
import os


app = Flask(__name__, template_folder='templates')


app.secret_key=os.environ["SECRET_KEY"];


@app.route("/")
def render_main():
    print("RunningMain")
    return render_template('page1.html')
@app.route('/page1',methods=['GET','POST'])
def renderPage1():
    session["firstName"]=request.form['firstName']
    session["lastName"]=request.form['lastName']
    return render_template('page1.html')
@app.route("/page2")
def renderPage2():
    return render_template('page2.html')
  
if __name__ == "__main__":
    app.run(debug=True)
