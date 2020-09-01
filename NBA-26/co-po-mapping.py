import pandas as pd
from pymongo import MongoClient
import pprint
import numpy as np
import itertools
import json
import dbAccess

# myclient = MongoClient('88.99.143.82',47118)
# db = myclient['dhi_analytics']
# db.authenticate('analytics','pPM8FUJflenw')


dbdetails = dbAccess.details()
myclient = MongoClient(dbdetails["host"],dbdetails["port"])
db = myclient[dbdetails["dbName"]]
db.authenticate(dbdetails["user"], dbdetails["password"])



def getCOForPO(year,term,batchNo,courseCode,section,poNumber):
    co_for_po = db.dhi_generic_attainment_data.aggregate(
        [
            {
                '$unwind': {
                    'path': '$courseOutcomeDetailsForAttainment'
                }
            }, {
                '$match': {
                    'year': year,
                    'termNumber': term,
                    'courseDetails.courseCode': courseCode,
                    'section': section,
                    'batchNumber': batchNo,
                    'isAssessmentYear': True
                }
            }, {
                '$unwind': {
                    'path': '$courseOutcomeDetailsForAttainment.coursePoMapAndAttainment'
                }
            }, {
                '$match': {
                    'courseOutcomeDetailsForAttainment.coursePoMapAndAttainment.programOutcomeNumber': poNumber
                }
            }, {
                '$project': {
                    '_id': 0,
                    'CO Number': '$courseOutcomeDetailsForAttainment.coNumber', 
                    'Total Attained Value': '$courseOutcomeDetailsForAttainment.coursePoMapAndAttainment.poTargetValue', 
                    'Mapping Level': '$courseOutcomeDetailsForAttainment.coursePoMapAndAttainment.poTargetLevel', 
                    'Score': '$courseOutcomeDetailsForAttainment.coursePoMapAndAttainment.poAttainment'
                }
            }
        ]
    )
    return list(co_for_po)

#arguments
year="2019-20"
semester="7"
batch=1
course="15CSL77"
section="B"
poNo="PO 2"
poName="Problem analysis"

#fucntion call
co_table=(getCOForPO(year,semester,batch,course,section,poNo))

#function check
if(len(co_table)==0):
    print("NO CO-PO Attainment")
else:
    pprint.pprint(co_table)
    # keys = []
    # vals = []
    # for data in co_table:
    #     val = []
    #     for k,v in data.items():
    #         keys.append(k)
    #         val.append(v)
    #     vals.append(val)
    # print(f" {poNo} : {poName}")
    # df=pd.DataFrame([v for v in vals], columns=list(dict.fromkeys(keys)))
    # print(df.to_string(index=False))