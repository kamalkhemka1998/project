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


@app.route("/courseCodes")
def get_course_codes():
    course_codes = st_17.get_course_of_faculty()
    return jsonify({"res":course_codes})

@app.route("/courseAttainmentData")
def get_course_attainment_data():
    course_attainment_data = st_17.get_course_attainment_information()
    return jsonify({"res":course_attainment_data})

@app.route("/courseAttainmentConfiguration")
def get_course_attainment_configuration():
    course_attainment_configuration = st_17.get_course_attainment_configuration()
    return jsonify({"res":course_attainment_configuration})

if __name__ == "__main__":
    app.run(debug=True) 

