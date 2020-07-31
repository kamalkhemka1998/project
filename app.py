from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import statement17 as st_17
from nba_16 import faculty_data as faculty
from mongoFlask import MongoJSON_Encoder

app = Flask(__name__)
app.json_encoder = MongoJSON_Encoder

@app.route("/terms")
def get_terms():
    terms_data = st_17.get_terms_details()
    return jsonify({"data":terms_data})

@app.route('/co_details_of_courses')
def get_cos_of_courses_of_a_faculty():
    course_codes = faculty.get_course_code()
    get_cos_of_courses = faculty.get_cos_of_courses(course_codes)
    return jsonify({'course_outcomes_faculty':get_cos_of_courses})

if __name__ == "__main__":
    app.run(debug=True) 

