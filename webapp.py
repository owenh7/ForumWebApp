from flask import Flask, request, Markup, render_template, flash, Markup
import os

app = Flask(__name__, template_folder='templates')


@app.route("/")
def render_main():
    print("RunningMain")
    with open('medal_of_honor.json') as medal_data:
        names = json.load(medal_data)
    return render_template('page1.html')
  @app.route("/p1")
def render_first():
    return render_template('page1.html')
@app.route("/p2")
def render_first2():
    return render_template('page2.html')
  
  if __name__ == "__main__":
    app.run(debug=True)
