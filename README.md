# Flask Healthcare Application

## Overview

This project involves creating a web application for collecting user survey data, storing it in MongoDB, processing the data, and deploying the application on an AWS EC2 instance. The survey collects information about users' income and spending patterns.

## Prerequisites

- AWS EC2 instance
- MongoDB Atlas account
- Basic knowledge of Python, Flask, and MongoDB
- MongoDB Compass (optional for managing MongoDB data)

## Setup and Deployment Instructions

### 1. **Setting Up MongoDB Atlas**

1. **Create a MongoDB Atlas Account:**
   - Sign up for a free MongoDB Atlas account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

2. **Create a Cluster:**
   - Navigate to the MongoDB Atlas dashboard and create a new cluster. Choose the free tier for no cost.

3. **Create a Database User:**
   - Go to the "Database Access" tab and create a new user with read and write access to your database.

4. **Whitelist Your IP Address:**
   - Navigate to "Network Access" and add your IP address or allow access from all IPs (not recommended for production).

5. **Obtain the Connection String:**
   - Go to the "Clusters" tab, click "Connect," and copy the connection string. Replace the placeholder values with your database username and password.

### 2. **Setting Up AWS EC2**

1. **Launch an EC2 Instance:**
   - Log in to the [AWS Management Console](https://aws.amazon.com/console/).
   - Navigate to EC2 and launch a new instance. Select an appropriate instance type (e.g., t2.micro for the free tier).
   - Choose an Amazon Machine Image (AMI), such as Ubuntu Server.
   - Configure instance details, storage, and security groups. Ensure port 5000 is open for Flask application access.

2. **Connect to Your EC2 Instance:**
   - Obtain the public IP address of your EC2 instance from the EC2 dashboard.
   - Connect to your instance using SSH:
     ```bash
     ssh -i /path/to/your-key.pem ec2-user@your-ec2-instance-public-dns
     ```
     Replace /path/to/your-key.pem with the actual path to your key file and your-ec2-instance-public-dns with your EC2 instance's public DNS or IP.

### 3. **Setting Up Your EC2 and Python Environment**

1. **Update and Install Necessary Packages:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install python3-pip python3-venv -y

2. **Create a virtual Environment for your Flask Application
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   Install Flask, pymongo, and gunicorn in the virtual environment:
   ```bash
   pip install Flask pymongo gunicorn
   ```
   Install other dependencies like dnspython for MongoDB:
   ```bash
   pip install dnspython
   ```

   
2. **Install Flask and PyMongo:**
   ```bash
   pip3 install Flask pymongo

### 4. **Deploying the Flask Application**

1. **Create the Flask Application:**
   Navigate to your directory
   ```bash
   cd /path/to/your/project-directory
   ```
   Use the nano text editor to add the code. Use ```CTRL + O``` to save the changes, press ```ENTER``` and use ```CTRL + X``` to exit
   ```bash
   nano app.py
   ```
   Save the following code as ```app.py```
  ```python
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
             def save_to_csv(self, filename='survey_data.csv'):
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

```

2. **Create the Flask Application:**
   Create a new template directory
   ```bash
   cd /path/to/your/project-directory
   mkdir templates
   ```
   Save the following code as ```survey.html```
  ```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Survey Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        form {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        h2 {
            text-align: center;
        }
        label {
            display: block;
            margin: 15px 0 5px;
        }
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .checkbox-group {
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
        }
        input[type="checkbox"] {
            margin-right: 10px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <h2>Income and Expense Survey</h2>
    <form action="/submit" method="POST">
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required>

        <label for="gender">Gender:</label>
        <select id="gender" name="gender" required>
            <option value="" disabled selected>Select your gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
        </select>

        <label for="total_income">Total Income:</label>
        <input type="number" id="total_income" name="total_income" required>

        <label for="expenses">Select your expenses and specify the amount:</label>
        <div class="checkbox-group">
            <label><input type="checkbox" name="expenses[utilities]" value="1"> Utilities: <input type="number" name="utilities" placeholder="Amount spent"></label>
            <label><input type="checkbox" name="expenses[entertainment]" value="1"> Entertainment: <input type="number" name="entertainment" placeholder="Amount spent"></label>
            <label><input type="checkbox" name="expenses[school_fees]" value="1"> School Fees: <input type="number" name="school_fees" placeholder="Amount spent"></label>
            <label><input type="checkbox" name="expenses[shopping]" value="1"> Shopping: <input type="number" name="shopping" placeholder="Amount spent"></label>
            <label><input type="checkbox" name="expenses[healthcare]" value="1"> Healthcare: <input type="number" name="healthcare" placeholder="Amount spent"></label>
        </div>

        <button type="submit">Submit Survey</button>
    </form>
</body>
</html>
```
Check that the ```survey.html``` is in the ```templates``` directory
```bash
ls templates
```

3. **Run the Flask Application:**
   ```bash
   python3 app.py
   ```
   You should now be able to access the form through your Flask app by visiting your EC2 public IP address in the browser.

   
5. **Downlooad the ```survey_data.csv``` from the EC2 by running this code**
   ```bash
   scp -i /path/to/your-key.pem ec2-user@your-ec2-public-ip:/path/to/your-flask-app/survey_data.csv /your/local/directory/
   ```
   or downloading FileZilla as a GUI to manage the files and download easily
