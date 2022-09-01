from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/survey", methods=("GET", "POST"))
def survey():
    if request.method == "POST":
        print(request.form.values())
        for value in request.form.values():
            print(value)
        return redirect(url_for("results"))
    return render_template("survey.html")


@app.route("/results")
def results():
    return "<p>results go here<p>"