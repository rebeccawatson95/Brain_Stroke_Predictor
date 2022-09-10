from pyexpat import model
from flask import Flask, render_template, request, url_for, redirect, flash
import pandas as pd
from ast import literal_eval
import model_script


app = Flask(__name__)

# Creating machine learning model
model = model_script.make_model()

r = False
res = ''

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/survey", methods=("GET", "POST"))
def survey():

    r = False
    res = ''
    if request.method == "POST":
        # print(request.to_dict())
        # print(request.form.values())
        # pd.DataFrame(request.form.values(), columns=request.form.keys())
        # pd.head()
        values = []
        keys = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
       'Residence_type', 'avg_glucose_level', 'bmi', 'work_type_Govt_job',
       'work_type_Never_worked', 'work_type_Private',
       'work_type_Self-employed', 'work_type_children',
       'smoking_status_Unknown', 'smoking_status_formerly smoked',
       'smoking_status_never smoked', 'smoking_status_smokes']

        for value in request.form.values():
            value = literal_eval(value)
            if isinstance(value, list):
                values = values + value
            else:
                values.append(value)
            #print(type(value))
        #print(values)
        input = pd.DataFrame.from_dict({'input':values}, orient="index", columns=keys)
        #print(input.dtypes)

        scaled = model_script.scale_input(input)
        pred = model.predict(scaled)
        r = True

        if pred[0] == 0:
            res = 'You are not likely to have a stroke'
        else:
            res = 'You are likely to have a stroke'
            
        #res = f'Your prediction is: {pred[0]}'
        #print(res)
        
        return render_template("survey.html", show_example_modal=r, res=res)

        #return redirect(url_for("results", pred=pred))
    
    return render_template("survey.html", show_example_modal=r, res=res)


if __name__ == '__main__':
    app.run(debug=True)