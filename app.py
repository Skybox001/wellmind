from flask import Flask, render_template, request, jsonify,redirect, url_for, session, flash
import numpy as np
import pandas as pd
import joblib
from chat import get_response
import mysql.connector

from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = '757106'

# Load the trained SVM model
svm_model = joblib.load('svm_model.pkl')

# Function to predict using the SVM model
def predict(data):
    # Make predictions
    predictions = svm_model.predict(data)
    
    return predictions

# Function to provide guidance and support
def provide_guidance(prediction):
    if prediction == 1:
        guidance_message = "You may be experiencing some mental health challenges. It's important to reach out for support from a mental health professional. Remember, you are not alone, and there are many resources available to help you through this."
    else:
        guidance_message = "Based on the information provided, you seem to be doing well at the moment. Continue taking care of yourself and don't hesitate to seek help if you ever feel the need. Your well-being is important."
    
    return guidance_message


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rawat@1234",
        database="chatbot"
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash("Signup successful, please login.")
            return redirect(url_for('login'))
        except:
            flash("Username already exists.")
        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))

        else:
            flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('self_check.html')


@app.route('/self_check')
def self_check():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    bot_response = get_response(user_text)
    return jsonify(bot_response)




@app.route('/predict_mental_status', methods=['POST'])
def predict_mental_status():
    input_data = {
        'Education': request.form['Education'],
        'Computer': request.form['Computer'],
        'Hospitalized': request.form['Hospitalized'],
        'legally_disabled': request.form['legally_disabled'],
        'live_with_parents': request.form['live_with_parents'],
        'gap_in_resume': request.form['gap_in_resume'],
        'Annual_income': float(request.form['Annual_income']),
        'unemployed': request.form['unemployed'],
        'Lack_of_concentration': request.form['Lack_of_concentration'],
        'Anxiety': request.form['Anxiety'],
        'Depression': request.form['Depression'],
        'Obsessive thinking': request.form['Obsessive thinking'],
        'Panic attacks': request.form['Panic attacks'],
        'Compulsive behavior': request.form['Compulsive behavior'],
        'Age': request.form['Age'],  # Include Age
        'Gender':request.form['Gender'],
    }

    # Create DataFrame from input data
    input_df = pd.DataFrame([input_data])
    
    # Predict
    prediction = predict(input_df.copy())[0]  # Get the first prediction from the list

    # Determine the result message
    result_message = "You May Need Support" if prediction == 1 else "You Seem to Be Doing Well"

    # Provide guidance message
    guidance_message = provide_guidance(prediction)

    show_whatsapp_call=prediction ==1

    return render_template('index.html', result_message=result_message, guidance_message=guidance_message,
                           show_whatsapp_call=show_whatsapp_call)
    
if __name__ == '__main__':
    app.run(debug=True)
