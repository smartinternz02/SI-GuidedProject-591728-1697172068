
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model1 = pickle.load(open("SW.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route('/predict')
def index():
    return render_template('index.html')

@flask_app.route("/predict", methods=["POST"])
def predict():
    # Retrieve the form data
    brand = request.form['Brand']
    model = request.form['Model']
    os = request.form.get('Operating_System', 'Default_Value')
    connect = request.form.get('Connectivity', 'Default_Value')
    display_type = request.form['Display_Type']
    display_size=request.form['Display_Size_inches']
    height = request.form['height']
    weight=request.form['weight'] 
    water_resistance=request.form['Water_Resistance_meters']
    battery_life=request.form['Battery_Life_days']
    heart_rate=request.form['Heart_Rate_Monitor']
    gps=request.form['GPS']
    nfc=request.form['NFC']
    # Create a DataFrame with the form data
    data = pd.DataFrame({
        'Brand': [brand],
        'Model': [model],
        'Operating_System': [os],
        'Connectivity': [connect],
        'Display_Type': [display_type],
        'Display_Size_inches':[display_size],
        'height':[height],
        'weight':[weight],
        'Water_Resistance_meters':[water_resistance],
        'Battery_Life_days':[battery_life],
        'Heart_Rate_Monitor':[heart_rate],
        'GPS':[gps],
        'NFC':[nfc]
        
    })

    # Perform one-hot encoding for categorical variables
    data = pd.get_dummies(data, columns=['Brand', 'Model', 'Operating_System', 'Connectivity', 'Display_Type','Heart_Rate_Monitor','GPS','NFC'])
    # Use the one-hot encoded data for prediction
    selected_features = data.iloc[:, :6]
    prediction = model1.predict(selected_features)

    # Round the prediction to two decimal places
    prediction = np.round(prediction, 2)

    return render_template('index.html', prediction_text="The prediction is {}".format(prediction))

if __name__ == '__main__':
    flask_app.run(debug=True)