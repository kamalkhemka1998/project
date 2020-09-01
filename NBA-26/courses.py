import pandas as pd
from pymongo import MongoClient
import pprint as pp
import numpy as np
import itertools
import json


# import DbAccess
myclient = MongoClient('88.99.143.82',47118)
db = myclient['dhi_analytics']
db.authenticate('analytics','pPM8FUJflenw')



# ay = "2018-19"
# tl = ["5","6"]
# det = "CS"
# em = "hod_biotech@pace.edu.in"
# rl = "FACULTY"

def faculty(email):

    facultylist = [x for x in db.dhi_user.aggregate([

        {
            "$match":
            {
                "email":email,
            }
        },
        {
            "$project":
            {
               "facultyGivenId": "$employeeGivenId",
               "degreeId": "$degreeId",
               "facultyName": "$name",
               "roles":"$roles.roleName",
               "deptId":"$deptId",
                "_id":0
            }
        }
    ])]
    return facultylist

def getFacultyAttainmentData(email,academic_year,term_list):
    result = []
    faculty_Id = faculty(email)[0]['facultyGivenId']
    department = faculty(email)[0]['deptId']
    roles = faculty(email)[0]['roles']
    print(roles)
    if "HOD" in roles:
        courses = db['dhi_lesson_plan'].aggregate([
        {
            '$unwind': {
                'path': '$faculties'
            }
        }, {
            '$unwind': {
                'path': '$departments'
            }
        }, {
            '$match': {
                'academicYear': academic_year, 
                'departments.deptId': department, 
                'departments.termNumber': {
                    '$in': term_list
                }
            }
        }, {
            '$group': {
                '_id': {
                    'academicYear': '$acdemicYear',
                    'termNumber': '$departments.termNumber', 
                    'section': '$departments.section', 
                    'semester': '$departments.termName', 
                    'courseName': '$courseShortName',
                    'courseCode' : '$courseCode'
                }
            }
        }
        ])
        for course in courses:
            print(course["_id"])
            result.append(course["_id"])
        
    else:
        courses = db['dhi_lesson_plan'].aggregate([
            {
                '$unwind': {
                    'path': '$faculties'
                }
            }, {
                '$unwind': {
                    'path': '$departments'
                }
            }, {
                '$match': {
                    'faculties.facultyId': faculty_Id, 
                    'academicYear': academic_year, 
                    'departments.termNumber': {
                        '$in': term_list
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'academicYear': '$acdemicYear',
                        'termNumber': '$departments.termNumber', 
                        'section': '$departments.section', 
                        'semester': '$departments.termName',
                        'courseName': '$courseShortName',
                        'courseCode' : '$courseCode'
                    }
                }
            }
        ])
        for course in courses:
            print(course["_id"])
            result.append(course["_id"])
        
    return result

def getAllAttainmentData(academic_year,term_list,department):
    result = []
    courses = db['dhi_lesson_plan'].aggregate([
        {
            '$unwind': {
                'path': '$faculties'
            }
        }, {
            '$unwind': {
                'path': '$departments'
            }
        }, {
            '$match': {
                'academicYear': academic_year, 
                'departments.deptId': department, 
                'departments.termNumber': {
                    '$in': term_list
                }
            }
        }, {
            '$group': {
                '_id': {
                    'academicYear': '$acdemicYear',
                    'termNumber': '$departments.termNumber', 
                    'section': '$departments.section', 
                    'semester': '$departments.termName', 
                    'courseName': '$courseShortName',
                    'courseCode' : '$courseCode'
                }
            }
        }
    ])
    for course in courses:
        print(course["_id"])
        result.append(course["_id"])
    return result



# getFacultyAttainmentData(em,ay,tl)


