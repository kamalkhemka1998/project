import pandas as pd
from pymongo import MongoClient
import pprint as pp
import numpy as np
import itertools
import json
import DbAccess
from flask import jsonify
from bson import json_util
from NBA21 import  faculty_attainment_data
dbdetails = DbAccess.details()
myclient = MongoClient(dbdetails["host"],dbdetails["port"])
db = myclient[dbdetails["dbName"]]
db.authenticate(dbdetails["user"], dbdetails["password"])

def get_bloomslevel_with_co(x):
    pipeline=    [
    {
        '$match': {
            'courseCode': x['courseCode'], 
            'academicYear': x['year'], 
            'faculties.facultyId': x['facultyId'], 
            'departments.termNumber': x['termNumber']
        }
    }, {
        '$unwind': {
            'path': '$plan'
        }
    }, {
        '$unwind': {
            'path': '$plan.couseOutcomes'
        }
    }, {
        '$unwind': {
            'path': '$departments'
        }
    }, {
        '$unwind': {
            'path': '$faculties'
        }
    }, {
        '$project': {
            '_id': 0, 
            'bloomsLevel': '$plan.bloomsLevel', 
            'coNumber': '$plan.couseOutcomes', 
            'courseName': 1, 
            'courseCode': 1, 
            'termNumber': '$departments.termNumber', 
            'section': '$departments.section', 
            'facultyId': '$faculties.facultyId',
            'academicYear': 1
        }
    }
    ] 
    
    mapping=db.dhi_lesson_plan.aggregate(pipeline);
    docs=[doc for doc in mapping]
    details=json.dumps(docs,default=json_util.default)

    df=pd.DataFrame(docs)
    df["bloomsLevel"]=df["bloomsLevel"].fillna("EMPTY")
    if df.empty:
        print("No data")
        return []
    bloomap={"EMPTY":0,"UNDERSTAND":2,"REMEMBER":1,"APPLY":3,"ANALYZE":4,"EVALUATE":5,"CREATE":6}
    bloominverse={1:"REMEMBER",2:"UNDERSTAND",3:"APPLY",4:"ANALYZE",5:"EVALUATE",6:"CREATE","EMPTY":0}
    res_table={}
    for i in range(1,df["coNumber"].max()+1):
        df1=df.loc[df["coNumber"]==i]
        if(~df1.empty):
            df1=df1.reset_index(drop=True)
            lst=[bloomap[df1.loc[j]["bloomsLevel"]]  for j in range(len(df1))]
            average=int(round(sum(lst)/len(lst)))
            res_table[df1["coNumber"][0]]=bloominverse[average]
    
    resd= pd.DataFrame(list(res_table.items()),columns = ['coNumber','BloomsLevel'])
    resd["courseCode"]=df["courseCode"][0]
    res_j=json.loads(resd.reset_index().to_json(orient="records"))
    # print(res_j)
    # res_j=[]
    return res_j

    

def get_map_blooms_to_co(facultyId,termList,year):
    pipeline=[
        {'$unwind':'$faculties'},
        {'$unwind':'$departments'},
        {'$match':
            {
            'faculties.facultyId':facultyId,
            'academicYear':year,
            'departments.termNumber':{'$in':termList}
        
            }
        },
        {
        '$project':
            {
                '_id':0,
                'courseCode':1,
                'courseName':1,
                'termNumber':'$departments.termNumber',
                'section':'$departments.section',
                'facultyId':'$faculties.facultyId',
                'year':'$academicYear',
            } 
        }
        ]
    mapping=db.dhi_lesson_plan.aggregate(pipeline)
    docs=[doc for doc in mapping]
    details=json.dumps(docs,default=json_util.default)
    df=pd.DataFrame(docs)
    print(df)
    blooms_level_mapping=[]
    if df.empty:
        return blooms_level_mapping
    blooms_level_mapping=[get_bloomslevel_with_co(df.loc[i]) for i in range(len(df))]
    return blooms_level_mapping

def get_overall_attainment_data(facultyId,termList,year):
    pipeline=[
        {'$unwind':'$faculties'},
        {'$unwind':'$departments'},
        {'$match':
            {
            'faculties.facultyId':facultyId,
            'academicYear':year,
            'departments.termNumber':{'$in':termList}
        
            }
        },
        {
        '$project':
            {
                '_id':0,
                'courseCode':1,
                'courseName':1,
                'termNumber':'$departments.termNumber',
                'section':'$departments.section',
                'facultyId':'$faculties.facultyId',
                'year':'$academicYear',
            } 
        }
        ]

    mapping=db.dhi_lesson_plan.aggregate(pipeline)
    docs=[doc for doc in mapping]
    details=json.dumps(docs,default=json_util.default)
    df=pd.DataFrame(docs)
    attainment_data = [faculty_attainment_data.get_attainment_details(df.loc[i]) for i in range(len(df))]
    print(attainment_data)
