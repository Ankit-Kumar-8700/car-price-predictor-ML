from flask import Flask,render_template,request
import joblib
import numpy as np
import pandas as pd

model = joblib.load('car_predict_save')
new_df = joblib.load('new_df_save')
train_df=joblib.load('train_df_save')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           Car_Name = list(new_df['Car_Name'].unique()),
                           Fuel_Type=list(new_df['Fuel_Type'].unique()),
                           Seller_Type=list(new_df['Seller_Type'].unique()),
                           Transmission=list(new_df['Transmission'].unique()),
                           Owner=list(new_df['Owner'].unique())
                           )

@app.route('/result',methods=['post'])
def recommend():
    Car_Name = request.form.get('Car_Name')
    Fuel_Type = request.form.get('Fuel_Type')
    Seller_Type = request.form.get('Seller_Type')
    Transmission = request.form.get('Transmission')
    Owner = request.form.get('Owner')
    age = request.form.get('age')
    Kms_Driven = request.form.get('Kms_Driven')
    Present_Price = request.form.get('Present_Price')
    columns=train_df.columns
    np_arr=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    prediction=pd.DataFrame(np_arr,columns=columns)
    try:
        print(type(Car_Name))
        print(type(Fuel_Type))
        print(type(Seller_Type))
        print(type(Transmission))
        print(type(Owner))
        print(type(age))
        print(type(Kms_Driven))
        print(type(Present_Price))

        prediction['Car_Name_'+Car_Name]=1.0
        prediction['Fuel_Type_'+Fuel_Type]=1.0
        prediction['Seller_Type_'+Seller_Type]=1.0
        prediction['Transmission_'+Transmission]=1.0
        prediction['Owner_'+Owner]=1.0
        prediction['age']=age
        prediction['Kms_Driven']=Kms_Driven
        prediction['Present_Price']=Present_Price
        final_answer=model.predict(prediction)[0]
        return render_template('result.html',final_answer=round(final_answer,2))
    except:
        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)