from flask import Flask, url_for, request, redirect, session, Markup, render_template, flash, Markup
from flask_oauthlib.client import OAuth
import os
import pymongo

def main():
    connection_string = os.environ["MONGO_CONNECTION_STRING"]
    db_name = os.environ["MONGO_DBNAME"]

    client = pymongo.MongoClient(connection_string)
    db = client[db_name]
    collection = db['Test']

app = Flask(__name__, template_folder='templates')


app.secret_key=os.environ["SECRET_KEY"];
oauth = OAuth(app)
oauth.init_app(app)


github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)


@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}


@app.route("/")
def render_main():
    print("RunningMain")
    return render_template('page1.html')
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))
@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            #pprint.pprint(vars(github['/email']))
            #pprint.pprint(vars(github['api/2/accounts/profile/']))
            message='You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            session.clear()
            print(inst)
            message='Unable to login, please try again.  '
    return render_template('page2.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/page1')
@app.route('/startOver')
def startOver():
    session.clear() 
    return redirect('/page1')
@app.route('/page1',methods=['GET','POST'])
def renderPage1():
    return render_template('page1.html')
@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    
    if 'user_data' in session:  
        post=request.form['Submit']
        MyDict={"text":post}
        insert_one(MyDict)
    else:
        return render_template('page3.html')
@app.route('/page1',methods=['GET','POST'])
def renderPage3():
    return render_template('page3.html')
   

@github.tokengetter
def get_github_oauth_token():
    return session['github_token']

  
if __name__ == "__main__":
    app.run(debug=True)
