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
     ssh -i "your-key.pem" ubuntu@<your-ec2-public-ip>
     ```

### 3. **Setting Up Your EC2 Environment**

1. **Update and Install Necessary Packages:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-dev mongodb-clients
