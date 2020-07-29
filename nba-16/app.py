from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import faculty_data as faculty

app = Flask(__name__)

@app.route('/course')
def get_info_of_users():
    course_codes = faculty.get_course_code()
    return jsonify({'course_codes':course_codes})

if __name__ == "__main__":
    app.run(debug=True)