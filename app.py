from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import statement17 as st_17
from mongoFlask import MongoJSON_Encoder

app = Flask(__name__)
app.json_encoder = MongoJSON_Encoder

@app.route("/terms")
def get_terms():
    terms_data = st_17.get_terms_details()
    return jsonify({"data":terms_data})

if __name__ == "__main__":
    app.run(debug=True) 

