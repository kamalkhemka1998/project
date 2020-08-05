from flask import Flask, jsonify, request
# from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import statement17 as st_17
from nba_16 import faculty_data as faculty
from nba_16 import hod_data as hod
import json
#from mongoFlask import MongoJSON_Encoder

app = Flask(__name__)
#app.json_encoder = MongoJSON_Encoder
cors = CORS(app)

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

@app.route('/hod/academicyear')
def get_academicYear_hod(dept_hod = 'CS' ,employeeGivenId = '583'):
    hod_academicYear = st_17.get_academicYear_hod(dept_hod) 
    return jsonify({"hod_academicYear":hod_academicYear})

@app.route('/hod/terms')
def get_term_hod(academicYear = "2018-19",dept = 'CS'):
    data = st_17.get_terms_hod(academicYear,dept)
    return jsonify( { "hod_terms" : data} )

@app.route('/hod/academicYear/dept')
# lists all the facultyId in hod's dept, invokes the method... works for principal too, only that we needn't find dept it'll be choosen
def get_facultyId_dept(academicYear = '2018-19', dept='CS',terms = ['3','5']):
    data = st_17.get_facultyId(academicYear,dept,terms)
    faculty_ids = data[0]['faculty_id'] 
    hod_data = []
    for fid in faculty_ids:
        course_details = st_17.get_course_of_faculty(fid,academicYear,terms)
        for j in range(len(course_details)):
            courseCode = course_details[j]['courseCode']
            section = course_details[j]['departments']['section']
            term = course_details[j]['departments']['termNumber']
            course_details[j]["facultyId"] = fid
            course_details[j]["Co_details"] = []
            course_attainment_details = st_17.get_course_attainment_information(academicYear,term,courseCode,section,fid)
            blooms_level = st_17.get_bloomsLevel_Of_Cos(fid, academicYear, term,courseCode)
            if course_attainment_details != []:
                for k in range(len(course_attainment_details[0]["uniqueValues"])):
                    course_details[j]["Co_details"].append(course_attainment_details[0]["uniqueValues"][k])
                    for co_num in range(1,7):
                        if course_details[j]["Co_details"][k]["coNumber"] == co_num:
                            course_details[j]["Co_details"][k]["blooms_details"] = blooms_level[co_num-1]
        hod_data.append(course_details)
    return jsonify({"hod_data": hod_data})

@app.route('/faculty/academicyear/<facultyGivenId>')
#facultyGivenId = '492'
def get_academicYear_faculty(facultyGivenId):
    faculty_academicYear = st_17.get_academicYear_faculty(facultyGivenId)
    return jsonify({"faculty_academicYear":faculty_academicYear})

@app.route("/faculty/terms/<facultyGivenId>/<academicYear>")
#facultyGivenId = '492',academicYear = '2018-19'
def get_terms_faculty(facultyGivenId,academicYear):
    faculty_terms_data = st_17.get_terms_faculty(facultyGivenId,academicYear)
    return jsonify({"faculty_terms":faculty_terms_data})

@app.route("/courseCodes")
def get_course_codes(facultyGivenId = '583',year = '2018-19',term = ['4'] ):
    course_codes = st_17.get_course_of_faculty(facultyGivenId,year,term)
    print(course_codes)
    return jsonify({"res":course_codes})

@app.route("/courseAttainmentData")
def get_course_attainment_information(year = '2018-19',term = ['4'],courseCode = '17CS42',section='A',facultyGivenId = '583'):
    course_attainment_data = st_17.get_course_attainment_information(year,term,courseCode,section,facultyGivenId)
    return jsonify({"res":course_attainment_data})

@app.route("/courseAttainmentConfiguration")
def get_course_attainment_configuration(year = '2018-19',dept = 'CS',courseCode = '17CS42'):
    course_attainment_configuration = st_17.get_course_attainment_configuration(year,dept,courseCode)
    return jsonify({"res":course_attainment_configuration})

@app.route('/faculty/co_details/<facultyId>/<academicYear>/<termNumber>')
def get_cos_of_courses_of_a_faculty(facultyId,academicYear,termNumber):
    termNumber = list(termNumber.split(','))
    get_cos_of_courses = faculty.get_cos_of_courses(facultyId,academicYear,termNumber)
    return jsonify({'course_outcomes_faculty':get_cos_of_courses})
    
@app.route('/co_details_of_dept_course')
def get_cos_of_courses_of_department():
    get_cos_of_courses_of_dept = hod.get_cos_of_all_courses_of_a_dept()
    return jsonify({'cos_of_courses_of_dept':get_cos_of_courses_of_dept})

@app.route('/assessment')
def get_info_of_co():
    test_co_details = faculty.get_co_data()
    return jsonify({'test_co_details':test_co_details})

@app.route('/getBlooms/<facultyId>/<academicYear>/<deptNumber>/<courseCode>')
def get_bloomsLevel_of_cos(facultyId,academicYear,deptNumber,courseCode):
    blooms = st_17.get_bloomsLevel_Of_Cos(facultyId,academicYear,deptNumber,courseCode)
    return jsonify({"res":blooms})

if __name__ == "__main__":
    app.run(debug=True) 

