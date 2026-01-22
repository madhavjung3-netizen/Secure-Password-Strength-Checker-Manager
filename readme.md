# **Secure Password Strength Checker & Manager**

## **Project Overview**

This project is a secure password management prototype built using **DevSecOps principles**. It features a password strength analyzer that uses entropy calculation and the "Have I Been Pwned" API (via k-Anonymity) to detect compromised credentials before they are stored. The application implements Role-Based Access Control (RBAC) and Time-Based One-Time Password (TOTP) Two-Factor Authentication (2FA).

Course: Cybersecurity Implementation & Best Practices (ICT932)  
Assessment: Project 4

## **Features**

* **Secure Authentication:** Flask-Login with Bcrypt hashing (12 rounds).  
* **2FA:** TOTP integration compatible with Google Authenticator/Authy.  
* **RBAC:** Admin and User roles with protected route decorators.  
* **Password Analysis:** zxcvbn entropy checks \+ HIBP Breach detection.  
* **Security Pipeline:** Integrated CI/CD with Bandit (SAST), Safety (SCA), and OWASP ZAP (DAST).

## **Technology Stack**

* **Backend:** Python 3.9+, Flask  
* **Database:** SQLite (SQLAlchemy ORM)  
* **Frontend:** Bootstrap 5, Jinja2 Templates  
* **Testing:** Pytest, Bandit, Safety

## **Installation & Setup**

### **1\. Prerequisites**

* Python 3.9 or higher installed.  
* Git installed.

### **2\. Clone Repository**

git clone \[https://github.com/yourusername/Password\_Manager\_Project.git\](https://github.com/yourusername/Password\_Manager\_Project.git)  
cd Password\_Manager\_Project

### **3\. Virtual Environment**

It is recommended to use a virtual environment to manage dependencies.

**Windows:**

python \-m venv venv  
venv\\Scripts\\activate

**Mac/Linux:**

python3 \-m venv venv  
source venv/bin/activate

### **4\. Install Dependencies**

pip install \-r requirements.txt

## **Running the Application**

### **1\. Start the Server**

python run.py

The application will start on http://127.0.0.1:5001.

### **2\. First Time Login**

1. Go to **Register**.  
2. Create an account (e.g., admin, admin@secure.com).  
3. **Scan the QR Code** with Google Authenticator (or any TOTP app) on your phone.  
4. Log in using the email, password, and the 6-digit code from your app.

## **Running Tests**

### **Functional Tests (Pytest)**

Run the unit tests to verify login, registration, and 2FA logic:

python run\_tests.py

### **Security Scans**

**Static Analysis (Bandit):**

bandit \-r src/

**Dependency Check (Safety):**

safety check \--full-report

## **CI/CD Pipeline**

This repository includes a GitHub Actions workflow .github/workflows/main.yml that automatically:

1. Builds the environment.  
2. Runs Security Scans (Bandit & Safety).  
3. Runs Unit Tests.  
4. Simulates Deployment.