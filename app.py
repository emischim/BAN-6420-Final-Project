from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import csv
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://emmanuel:Mainasara777*@cluster1.pnm5w.mongodb.net/flask_db?retryWrites=true&w=majority")
db = client["flask_db"]
collection = db["user_data"]

# Define the User class
class User:
    def __init__(self, age, gender, total_income, expenses):
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses

    # Method to save user data to MongoDB
        # Method to save user data to MongoDB
    def save_to_mongo(self):
        try:
            # Re-attempt connection to MongoDB before saving
            client = MongoClient("mongodb+srv://emmanuel:Mainasara777*@cluster1.pnm5w.mongodb.net/flask_db?retryWrites=true&w=majority")
            db = client["flask_db"]
            collection = db["user_data"]
            
            # Insert the data
            data = {
                'age': self.age,
                'gender': self.gender,
                'total_income': self.total_income,
                'expenses': self.expenses
            }
            collection.insert_one(data)
            print("Data saved to MongoDB successfully.")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")

    # Method to save user data to CSV
    def save_to_csv(self, filename='user_data.csv'):
        # Check if the file exists
        file_exists = os.path.isfile(filename)
        
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # If the file doesn't exist, write the headers
            if not file_exists:
                writer.writerow(['Age', 'Gender', 'Total_Income', 'Expenses'])
            
            # Write the user data
            writer.writerow([self.age, self.gender, self.total_income, self.expenses])

# Home page route to render the form
@app.route('/')
def survey_form():
    return render_template('survey.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit_data():
    age = request.form['age']
    gender = request.form['gender']
    total_income = request.form['total_income']
    expenses = {
        'utilities': request.form.get('utilities'),
        'entertainment': request.form.get('entertainment'),
        'school_fees': request.form.get('school_fees'),
        'shopping': request.form.get('shopping'),
        'healthcare': request.form.get('healthcare')
    }

    # Create a User object
    user = User(age, gender, total_income, expenses)

    # Save to MongoDB
    user.save_to_mongo()

    # Save to CSV
    user.save_to_csv()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
