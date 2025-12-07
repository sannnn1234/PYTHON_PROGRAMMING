# Python Programming Assignment

## **Q1. Password Strength Checker**

### **Requirements**

A password must meet the following criteria:

* Minimum length: **8 characters**
* Contains **uppercase** and **lowercase** letters
* Contains at least **one digit (0–9)**
* Contains at least **one special character** (e.g., `! @ # $ %`)

### **Python Implementation**

```python
import re

def check_password_strength(password):
    # Check minimum length
    if len(password) < 8:
        return False

    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # Check for at least one digit
    if not re.search(r"[0-9]", password):
        return False

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


password = input("Enter a password to check its strength: ")

if check_password_strength(password):
    print("Strong Password")
else:
    print("Weak Password! Make sure it:")
    print("Has at least 8 characters")
    print("Contains both UPPERCASE and lowercase letters")
    print("Contains at least one digit (0-9)")
    print("Contains at least one special character (!@#$ etc.)")
```

---

## **Q2. CPU Health Monitoring Script**

### **Objective**

Monitor real-time CPU usage to ensure system stability and detect high usage.

### **Key Functionality**

* Use the **psutil** library for system monitoring.
* Continuously check CPU usage.
* Display an **alert** if CPU usage crosses the **80% threshold**.
* Run indefinitely until manually stopped.
* Handle exceptions safely.

### **Python Implementation**

```python
import psutil
import time

CPU_THRESHOLD = 80  

print("Monitoring CPU usage...")

while True:
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > CPU_THRESHOLD:
            print(f"Alert! CPU usage exceeds threshold: {cpu_usage}%")
        # (Optional) slow down monitoring slightly
        time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        break

    except Exception as e:
        print(f"An error occurred: {e}")
        break
```

---

## **Q3. Configuration File Parser & JSON Storage**

### **Configuration File**

```
[Database]
host = localhost
port = 3306
username = admin
password = secret

[Server]
address = 192.168.0.1
port = 8080
```

### **Python Implementation**

```python
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import configparser

# Load env vars
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

CONFIG_FILE = "config.ini"  

# -------- Parse Config File -------- #
@app.route('/', methods=['GET'])
def parse_config():

    config = configparser.ConfigParser()

    # Error handling if file missing
    if not os.path.exists(CONFIG_FILE):
        return jsonify({"error": "config.ini file not found!"}), 404

    config.read(CONFIG_FILE)
    parsed_data = {}

    # Convert to dictionary
    for section in config.sections():
        parsed_data[section] = {}
        for key in config[section]:
            parsed_data[section][key] = config[section][key]

    # Save to MongoDB
    mongo.db.config_data.delete_many({})  # Clear old data
    mongo.db.config_data.insert_one(parsed_data)

    return jsonify({
        "message": "Configuration parsed & saved to MongoDB successfully!",
        "data": parsed_data
    })


# -------- Get Config From DB -------- #
@app.route('/get-config', methods=['GET'])
def get_config():

    data = mongo.db.config_data.find_one()

    if not data:
        return jsonify({"error": "No configuration data found in DB"}), 404

    # Remove MongoDB ObjectId
    data["_id"] = str(data["_id"])

    return jsonify({
        "message": "Configuration fetched successfully",
        "data": data
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8082)
```


