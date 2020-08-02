from flask import Flask, jsonify, request
# from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import statement17 as st_17
from nba_16 import faculty_data as faculty
# from mongoFlask import MongoJSON_Encoder

app = Flask(__name__)
# app.json_encoder = MongoJSON_Encoder

@app.route('/principal/academicyear')
def get_academicYear_principal():
    year = st_17.get_academicYear_principal()
    return jsonify({"year":year})

@app.route('/principal/department_term')
def get_dept_term_principal(academicYear = '2018-19'):
    data = st_17.get_dept_term_principal(academicYear)
    return jsonify({"dept_and_term":data})

@app.route('/hod/dept')
def dep_hod(employeeGivenId = '583'):
    dept_hod = st_17.get_dept_hod(employeeGivenId)
    return jsonify({"dept_hod":dept_hod})

@app.route('/hod/academicyear')
def get_academicYear_hod(dept_hod = 'CS' ,employeeGivenId = '583'):
    hod_academicYear = st_17.get_academicYear_hod(dept_hod) 
    return jsonify({"hod_academicYear":hod_academicYear})

@app.route('/hod/terms')
def get_term_hod(academicYear = "2018-19",dept = 'CS'):
    data = st_17.get_terms_hod(academicYear,dept)
    return jsonify( { "hod_terms" : data} )

@app.route('/faculty/academicyear')
def get_academicYear_faculty(facultyGivenId = '492'):
    faculty_academicYear = st_17.get_academicYear_faculty(facultyGivenId)
    return jsonify({"faculty_academicYear":faculty_academicYear})

@app.route("/faculty/terms")
def get_terms_faculty(facultyGivenId = '492',academicYear = '2018-19'):
    faculty_terms_data = st_17.get_terms_faculty(facultyGivenId,academicYear)
    return jsonify({"faculty_terms":faculty_terms_data})

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

@app.route('/co_details_of_courses')
def get_cos_of_courses_of_a_faculty():
    course_codes = faculty.get_course_code()
    get_cos_of_courses = faculty.get_cos_of_courses(course_codes)
    return jsonify({'course_outcomes_faculty':get_cos_of_courses})

@app.route('/assessment')
def get_info_of_co():
    test_co_details = faculty.get_co_data()
    return jsonify({'test_co_details':test_co_details})

if __name__ == "__main__":
    app.run(debug=True) 

