from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np

app = Flask(__name__)     # Create the Flask app

filename="./predictor.pickle"
with open(filename,'rb') as file:
        model = pickle.load(file)

def Prediction(list):
    filename="./predictor.pickle"
    with open(filename,'rb') as file:
        model = pickle.load(file)
    Prediction = model.predict([list])
    return Prediction

@app.route("/",methods=["POST","GET"])   # Define a route for the home page
def index():
    pred = "Diabetes Checker"
    if request.method =='POST':

        Pregnancies = request.form['pregnancies'] 
        Glucose	= request.form['glucose'] 
        BloodPressure =	request.form['bloodPressure'] 
        SkinThickness =	request.form['skinThickness'] 
        Insulin =	request.form['insulin'] 
        BMI =	request.form['bmi'] 
        DiabetesPedigreeFunction =	request.form['diabetesPedigreeFunction'] 
        Age = request.form['age'] 
        lst = []
        lst.append(int(Pregnancies))
        lst.append(int(Glucose))
        lst.append(int(BloodPressure))
        lst.append(float(SkinThickness))
        lst.append(float(Insulin))
        lst.append(float(BMI))
        lst.append(float(DiabetesPedigreeFunction))
        lst.append(int(Age))
        
        pred = Prediction(lst)
        if pred ==0:
            pred = "Luckily Patient has not Diabetes"
        elif pred ==1 :
            pred = "Unfortunately Patient has Diabetes"

    return render_template("index.html",pred= pred)


@app.route('/prediction', methods =["POST"])

def predict_api():
    data = request.json['data']
    new_data = np.array(list(data.values())).reshape(1,-1)
    out_put = model.predict(new_data)
    result = int(out_put[0])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)                # Run the app in debug mode.


    