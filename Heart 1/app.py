from flask import Flask,render_template,request,flash
import bsqlite3 
import sqlite3
import numpy as np 
import joblib
load_model = joblib.load("heart_disease.pkl")

app = Flask(__name__)
app.secret_key = 'Qazwx@123' #Replace with a strong,random key 


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")

def dbconnect():
    conn = sqlite3.connect("users.db")
    return conn

@app.route("/user_register",methods=['POST'])
def userdata():
    uname = request.form['name']
    age = request.form['age']
    gen = request.form['gender']
    contactnumber = request.form['contact']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    print(uname,age,gen,contactnumber,email, password,address)
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(name,age,gender,contactnumber,email,password,address)VALUES(?,?,?,?,?,?,?)",(uname,age,gen,contactnumber,email, password,address))
    conn.commit()
    conn.close()
    flash('Login Successful!','success')
    
    return render_template("login.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        print(username,password)
        conn=dbconnect()
        cursor=conn.cursor()
        cursor.execute("SELECT*FROM users WHERE name=? AND password=?",(username,password))
        user=cursor.fetchone()
        conn.close()  
        if user:
            return render_template("userhome.html")
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/predict",methods=['POST'])
def userhome():
    

    if request.method == 'POST':
        age= int(request.form.get('age'))
        sex= int(request.form.get('sex'))
        chestpain=int(request.form.get('cp',0))
        trestbps=int (request.form.get('trestbps'))
        chol= int(request.form.get('chol'))
        fbs=int(request.form.get('fbs'))
        restecg=int(request.form.get('restecg'))
        thalach=int(request.form.get('thalach'))
        exang=int(request.form.get('exang'))
        oldpeak=float(request.form.get('oldpeak'))
        slope=int(request.form.get('slope'))
        ca=int(request.form.get('idca'))
        thal= int(request.form.get('thal'))
        print(age,sex,chestpain,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
        input_data =np.array([[age,sex,chestpain,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        pred=load_model.predict(input_data)
        print(pred)
        print("____________________reached")
        if pred[0]==1:
            prediction="Heart disease is present"
            print(prediction)
        else:
            prediction="No heart disease"
            print(prediction)
    return render_template("userhome.html",prediction=prediction)    

 

if __name__ == "__main__":
   app.run(debug=True)

