from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)     # Create the Flask app

filename="./predictor.pickle"
with open(filename,'rb') as file:
        model = pickle.load(file)

def Prediction(list):

    Prediction = model.predict([list])
    return Prediction

@app.route("/",methods=["POST","GET"])   # Define a route for the home page
def index():
    pred = "Diabetes Checker"
    if request.method =='POST':
    
        Pregnancies = int(request.form['pregnancies'])
        Glucose = int(request.form['glucose'])
        BloodPressure = int(request.form['bloodPressure'])
        SkinThickness = float(request.form['skinThickness'])
        Insulin = float(request.form['insulin'])
        BMI = float(request.form['bmi'])
        DiabetesPedigreeFunction = float(request.form['diabetesPedigreeFunction'])
        Age = int(request.form['age'])


        lst = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
       
        pred = Prediction(lst)
        if pred == 0:
            pred = "Luckily Patient has not Diabetes"
        elif pred == 1 :
            pred = "Unfortunately Patient has Diabetes"

    return render_template("index.html",pred= pred)


@app.route('/prediction', methods =["POST"])

def predict_api():
    data = request.get_json()
    new_data = np.array(list(data.values())).reshape(1,-1)
    out_put = model.predict(new_data)
    result = int(out_put[0])
    return jsonify({"Prediction":result})



if __name__ == '__main__':
    # app.run(debug=True)   
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port, debug=True)             # Run the app in debug mode.


    