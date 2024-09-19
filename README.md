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
         from flask import Flask, request, render_template
         from pymongo import MongoClient
         from pymongo.errors import ConnectionError
         
         app = Flask(__name__)
         
         try:
             client = MongoClient("mongodb+srv://<your-username>:<your-password>@cluster1.pnm5w.mongodb.net/<your-db>?retryWrites=true&w=majority")
             db = client.surveyDB
             collection = db.surveyCollection
             print("MongoDB connection successful")
         except ConnectionError as e:
             print("MongoDB connection failed:", e)
             db = None
         
         @app.route('/')
         def index():
             return render_template('survey.html')
         
         @app.route('/submit', methods=['POST'])
         def submit():
             if db is None:
                 return render_template('survey.html', message="Failed to connect to database.")
         
             # Extract data from form
             age = int(request.form['age'])
             gender = request.form['gender']
             total_income = float(request.form['total_income'])
             expenses = {
                 "utilities": float(request.form.get('utilities', 0)) if request.form.get('expenses[utilities]') else 0,
                 "entertainment": float(request.form.get('entertainment', 0)) if request.form.get('expenses[entertainment]') else 0,
                 "school_fees": float(request.form.get('school_fees', 0)) if request.form.get('expenses[school_fees]') else 0,
                 "shopping": float(request.form.get('shopping', 0)) if request.form.get('expenses[shopping]') else 0,
                 "healthcare": float(request.form.get('healthcare', 0)) if request.form.get('expenses[healthcare]') else 0,
             }
         
             # Insert data into MongoDB
             collection.insert_one({
                 "age": age,
                 "gender": gender,
                 "total_income": total_income,
                 "expenses": expenses
             })
         
             # Render the form again with a success message
             return render_template('survey.html', message="Submitted")
         
            if __name__ == '__main__':
                app.run(host='0.0.0.0', port=5000, debug=True)
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

        {% if message %}
            <p style="color: green; text-align: center;">{{ message }}</p>
        {% endif %}
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
