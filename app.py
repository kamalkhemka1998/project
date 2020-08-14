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

@app.route('/principal/departments')
def get_dept_principal( ):
    data = st_17.get_dept_principal()
    return jsonify({"departments":data[0]['dept']})

@app.route('/hod/dept/<employeeGivenId>')
def dep_hod(employeeGivenId = '583'):
    dept_hod = st_17.get_dept_hod(employeeGivenId)
    return jsonify({"dept_hod":dept_hod})
    
@app.route('/hod/academicyear/<dept_hod>')
def get_academicYear_hod(dept_hod):
    hod_academicYear = st_17.get_academicYear_hod(dept_hod) 
    return jsonify({"hod_academicYear":hod_academicYear})

@app.route('/hod/terms/<academicYear>/<dept>')
def get_term_hod(academicYear,dept):
    data = st_17.get_terms_hod(academicYear,dept)
    return jsonify( { "hod_terms" : data} )

@app.route('/hod/details/<academicYear>/<dept>/<t>')
# lists all the facultyId in hod's dept, invokes the method... works for principal too, only that we needn't find dept it'll be choosen
def get_facultyId_dept(academicYear = '2018-19', dept='CS',t = '3'):
    terms = list(t.split(','))
    list_faculty = st_17.get_facultyId(academicYear,dept,terms)
    # print(list_faculty)
    hod_data = list()
    for fid in list_faculty[0]['faculty_id']:
        data = st_17.get_course_of_faculty(fid,academicYear, terms)
        for d in data:
<<<<<<< HEAD
            section = d['departments'][0]['section']        
            d['termNumber'] = d["departments"][0]["termNumber"]
            term = list(d["departments"][0]["termNumber"])
            d.pop('departments')
            d['section'] = section
            courseCode = d["courseCode"]
            courseO_att_info = st_17.get_course_attainment_information(academicYear,term,courseCode,section,fid)
=======
            courseO_att_info = st_17.get_course_attainment_information(academicYear,list(d['termNumber']),d["courseCode"],d['section'],fid)
>>>>>>> 7b0c3db95b4c0bf07a69d5c162991d8d7ea39ae5
            if len(courseO_att_info) != 0:
                for i in range(len(courseO_att_info[0]["uniqueValues"])):
                    for j in range(len(d["Co_details"])):
                        if d["Co_details"][j]['Difficulty'] == 0:
                            continue
                        if d["Co_details"][j]["CO"] == courseO_att_info[0]["uniqueValues"][i][ "coNumber"]:
                            # info = list(courseO_att_info[0]["uniqueValues"][i])
                            # d["Co_Details"][j].extend(info)
                            d["Co_details"][j]["co_difficultyLevel"] = courseO_att_info[0]["uniqueValues"][i]["Difficulty"] 
                            d["Co_details"][j]["indirectAttainment"] = courseO_att_info[0]["uniqueValues"][i]["indirectAttainment"] 
                            d["Co_details"][j]["totalAttainment"] = courseO_att_info[0]["uniqueValues"][i]["totalAttainment"]
                            d["Co_details"][j]["directAttainment"] = courseO_att_info[0]["uniqueValues"][i]["directAttainment"]
                            break
            else:
                for j in range(len(d["Co_details"])):
                    d["Co_details"][j]["co_difficultyLevel"] = 30
                    d["Co_details"][j]["indirectAttainment"] = 20
                    d["Co_details"][j]["totalAttainment"] = 40
                    d["Co_details"][j]["directAttainment"] = 50
                # courseO_att_info = st_17.get_course_attainment_configuration(academicYear,dept,courseCode)
            num_cos = len(d["Co_details"])
            sum_diff = 0
            for j in range( num_cos ):
                sum_diff += d["Co_details"][j]["Difficulty"]
            crs_diff_levl = sum_diff/num_cos 
            d["course_difficultyLevel_per"] = crs_diff_levl
            hod_data.append( d)
    return jsonify({"hod_data": hod_data})

@app.route('/faculty/academicyear/<facultyGivenId>')
#facultyGivenId = '492'
def get_academicYear_faculty(facultyGivenId):
    faculty_academicYear = st_17.get_academicYear_faculty(facultyGivenId)
    print(faculty_academicYear)
    return jsonify({"faculty_academicYear":faculty_academicYear})

@app.route("/faculty/terms/<facultyGivenId>/<academicYear>")
#facultyGivenId = '492',academicYear = '2018-19'
def get_terms_faculty(facultyGivenId,academicYear):
    faculty_terms_data = st_17.get_terms_faculty(facultyGivenId,academicYear)
    return jsonify({"faculty_terms":faculty_terms_data})

@app.route("/courseCodes/<fid>/<year>/<term>")
def get_course_codes(fid,year,term = ['4']):
    term = list(term.split(','))
    data = st_17.get_course_of_faculty(fid,year,term)
    faculty_data = list()
    for d in data:
<<<<<<< HEAD
        section = d['departments']['section']
        d['termNumber'] = d["departments"]["termNumber"]
        term = list(d["departments"]["termNumber"])
        d.pop('departments')
        d['section'] = section
=======
>>>>>>> 7b0c3db95b4c0bf07a69d5c162991d8d7ea39ae5
        courseCode = d["courseCode"]
        courseO_att_info = st_17.get_course_attainment_information(year,list(d['termNumber']),d["courseCode"],d['section'],fid)
        if len(courseO_att_info) != 0:
            for i in range(len(courseO_att_info[0]["uniqueValues"])):
                for j in range(len(d["Co_details"])):
                    if d["Co_details"][j]['Difficulty'] == 0:
                        continue
                    if d["Co_details"][j]["CO"] == courseO_att_info[0]["uniqueValues"][i][ "coNumber"]:
                        # info = list(courseO_att_info[0]["uniqueValues"][i])
                        # d["Co_Details"][j].extend(info)
                        d["Co_details"][j]["co_difficultyLevel"] = courseO_att_info[0]["uniqueValues"][i]["Difficulty"] 
                        d["Co_details"][j]["indirectAttainment"] = courseO_att_info[0]["uniqueValues"][i]["indirectAttainment"] 
                        d["Co_details"][j]["totalAttainment"] = courseO_att_info[0]["uniqueValues"][i]["totalAttainment"]
                        d["Co_details"][j]["directAttainment"] = courseO_att_info[0]["uniqueValues"][i]["directAttainment"]
                        break
        else:
            for j in range(len(d["Co_details"])):
                d["Co_details"][j]["co_difficultyLevel"] = 30
                d["Co_details"][j]["indirectAttainment"] = 20
                d["Co_details"][j]["totalAttainment"] = 40
                d["Co_details"][j]["directAttainment"] = 50
            # courseO_att_info = st_17.get_course_attainment_configuration(academicYear,dept,courseCode)
        num_cos = len(d["Co_details"])
        sum_diff = 0
        for j in range( num_cos ):
            sum_diff += d["Co_details"][j]["Difficulty"]
        crs_diff_levl = sum_diff/num_cos 
        d["course_difficultyLevel_per"] = crs_diff_levl
        faculty_data.append(d)
    return jsonify({"faculty": faculty_data})

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
    
@app.route('/co_details_of_dept_course/<academicYear>/<termNumber>/<deptId>')
def get_cos_of_courses_of_department(academicYear,termNumber,deptId):
    termNumber = list(termNumber.split(','))
    get_cos_of_courses_of_dept = hod.get_cos_of_all_courses_of_a_dept(academicYear,termNumber,deptId)
    return jsonify({'cos_of_courses_of_dept':get_cos_of_courses_of_dept})

@app.route('/faculty/data_table/<academicYear>/<facultyId>/<termNumber>/<section>/<courseCode>/<int:coNumber>/<deptId>/<courseType>')
def get_info_of_co(academicYear,facultyId,termNumber,section,courseCode,coNumber,deptId,courseType):
    test_co_details = faculty.get_co_data(academicYear,facultyId,termNumber,section,courseCode,coNumber,deptId,courseType)
    return jsonify({'test_co_details':test_co_details})

@app.route('/rubric_details/<academicYear>/<deptId>/<courseType>')
def get_rubric_details(academicYear,deptId,courseType):
    rubric_details = faculty.get_rubrics_details(academicYear,deptId,courseType)
    return jsonify({'rubric_detail':rubric_details})

@app.route('/getBlooms/<facultyId>/<academicYear>/<deptNumber>/<courseCode>')
def get_bloomsLevel_of_cos(facultyId,academicYear,deptNumber,courseCode):
    blooms = st_17.get_bloomsLevel_Of_Cos(facultyId,academicYear,deptNumber,courseCode)
    return jsonify({"res":blooms})

@app.route('/getTotalLessons/<fid>/<year>/<code>/term')
def get_totalLessons(fid,year,code,term=['4']):
    totalLessons = st_17.get_totalLessons_of_course_and_Co(fid,year,code,term)
    return jsonify({"res":totalLessons})

if __name__ == "__main__":
    app.run(debug=True) 

