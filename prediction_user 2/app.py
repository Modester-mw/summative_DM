import mysql.connector
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
import os
from flask import render_template
import time

app = Flask(__name__, template_folder=os.path.abspath('/Users/foundation/Desktop/prediction_user/templates'))

# create a connection to the database
cnx = mysql.connector.connect(user='root', password='Foundation30',
                              host='localhost',
                              database='enrollment')

@app.route('/')
def home():
   return render_template('home.html')
# Define a route for the prediction

@app.route('/predict', methods=['POST'])
def predict():
     # Establish a connection to the database
    cnx = mysql.connector.connect(user='your_username', password='your_password',
                              host='localhost',
                              database='enrollment')

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Execute a query to fetch the data
    query = "SELECT * FROM courses"
    cursor.execute(query)

    # Fetch the data and store it in a list
    courses = []
    for row in cursor.fetchall():
        courses.append(row[1])

    # Close the cursor and connection objects
    cursor.close()
    cnx.close()

    # Get the user inputs from the form
    course = request.form['course']
    status = request.form['status']
    current_courses = request.form['current_courses']
    scores = request.form['scores']
    time_spent = request.form['time_spent']

    # Create a new sample data
    new_data = pd.DataFrame({
        'Course Name_' + course: [1],
        'Course Status_' + status: [1],
        'Current Courses in Progress': [current_courses],
        'Score': [scores],
        'Time Spent': [time_spent]
    })

    # Convert score and time_spent columns to numeric type
    new_data['Score'] = pd.to_numeric(new_data['Score'], errors='coerce')
    new_data['Time Spent'] = pd.to_numeric(new_data['Time Spent'], errors='coerce')

    # Make the prediction using the trained model
    threshold = 0.5 # You can adjust this value as needed
    proba = model.predict_proba(new_data)[:, 1]
    prediction = 'Completed' if proba >= threshold else 'Dropout'

    # Return the prediction to the user
    return render_template('prediction.html', prediction=prediction)
