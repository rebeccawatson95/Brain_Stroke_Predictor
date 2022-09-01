from flask import Flask, render_template, request, url_for, redirect, flash
import pandas as pd
from ast import literal_eval

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/survey", methods=("GET", "POST"))
def survey():
    if request.method == "POST":
        # print(request.to_dict())
        # print(request.form.values())
        # pd.DataFrame(request.form.values(), columns=request.form.keys())
        # pd.head()
        values = []
        keys = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'stroke', 'gender', 'ever_married', 'work_type_Govt_job', 'work_type_Never_worked', 'work_type_Private', 'work_type_Self-employed', 'work_type_children', 'Residence_type', 'smoking_status_Unknown', 'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes']
        for value in request.form.values():
            value = literal_eval(value)
            if isinstance(value, list):
                values = values + value
            else:
                values.append(value)
            print(type(value))
        print(values)
        print(len(keys))
        print(len(values))
        return redirect(url_for("results"))
    return render_template("survey.html")


@app.route("/results")
def results():
    return "<p>results go here<p>"