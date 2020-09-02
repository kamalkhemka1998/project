import pandas as pd
from pymongo import MongoClient
import pprint as pp
import numpy as np
import itertools
import json
import DbAccess
from flask import jsonify
from bson import json_util
dbdetails = DbAccess.details()
myclient = MongoClient(dbdetails["host"],dbdetails["port"])
db = myclient[dbdetails["dbName"]]
db.authenticate(dbdetails["user"], dbdetails["password"])

def get_hod_dept(year,facultyId):
    pipeline= [
    {
        '$unwind': {
            'path': '$faculties'
        }
    }, {
        '$match': {
            'academicYear': year, 
            'faculties.facultyId': facultyId
        }
    }, {
        '$project': {
            'departments.deptId': 1, 
            '_id': 0
        }
    }
]

    mapping=db.dhi_lesson_plan.aggregate(pipeline)
    docs=[doc for doc in mapping]
    #details=json.dumps(docs,default=json_util.default)
    return(docs)

def get_term_hod_dept(deptId,year):
    pipeline=[
    {
        '$match': {
            'academicYear': year 
        }
    }, {
        '$unwind': {
            'path': '$faculties'
        }
    }, {
        '$match': {
            'departments.deptId': deptId
        }
    }, {
        '$unwind': {
            'path': '$departments'
        }
    }, {
        '$group': {
            '_id': '$departments.termNumber'
        }
    }
]

    mapping=db.dhi_lesson_plan.aggregate(pipeline)
    docs=[doc for doc in mapping]
    #details=json.dumps(docs,default=json_util.default)
    return(docs)
    