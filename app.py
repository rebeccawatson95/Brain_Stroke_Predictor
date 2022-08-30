from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/survey")
def survey():
    return "<p>survey go here<p>"

@app.route("/results")
def results():
    return "<p>results go here<p>"