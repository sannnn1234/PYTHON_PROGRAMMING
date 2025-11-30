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