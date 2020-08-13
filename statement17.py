from pymongo import MongoClient
# from flask_pymongo import PyMongo

db = MongoClient(host='localhost',port = 27017)

#mydatabase = db['nba-analytics-backend']
mydatabase = db['analytics']
generic_attainment_configuration = mydatabase['dhi_generic_attainment_configuration']
generic_attainment_data = mydatabase['dhi_generic_attainment_data']
lesson_plan = mydatabase['dhi_lesson_plan']
term_detail = mydatabase['dhi_term_detail']
dhi_user = mydatabase['dhi_user']


def get_dept_principal():
    query =lesson_plan.aggregate([
        {'$unwind': '$departments'},
        {'$group': {'_id': 'null', "dept":{"$addToSet":"$departments.deptId"}}},
        {'$project': {'_id':0, "dept":1}}
    ])
    return [q for q in query]

def get_dept_principal():
    query =lesson_plan.aggregate([
        {'$unwind': '$departments'},
        {'$group': {'_id': 'null', "dept":{"$addToSet":"$departments.deptId"}}},
        {'$project': {"dept":1,'_id':0}}
    ])
    return [q for q in query]


def get_dept_hod(employeeGivenId):
    query =dhi_user.find({"employeeGivenId":employeeGivenId}, {'_id':0, 'deptId' : 1 })
    return [q for q in query]

def get_academicYear_hod(dept):
    querry = lesson_plan.aggregate([
    { '$match' : {"faculties.facultyDeptId":dept}},
    {'$group': { '_id' : 'null',
        "all_academic_year" : {'$addToSet': "$academicYear"}
        }},
    {'$project' : {'_id' : 0, "all_academic_year":1}}
    ])
    return [q for q in querry]

def get_terms_hod(academicYear,dept):
    querry = lesson_plan.aggregate([
        {'$match' : {"departments.deptId" : dept, "academicYear":academicYear}},
        {'$project' : {'_id':0,"departments.termNumber":1}},
        {'$unwind' : "$departments"},
        {'$group' : {'_id' : 'null', "hod_terms":{'$addToSet' : "$departments.termNumber"}}},
        {'$project' : {'_id': 0}}
        ])
    return [q for q in querry] 

def get_facultyId(academicYear,dept,terms):
    query = lesson_plan.aggregate([
    {'$match' : {
    "academicYear":academicYear, "departments.termNumber":{ '$in' : terms}, "departments.deptId":dept}}, 
    {'$unwind': "$faculties"},
    {'$group' : { '_id': 'null', "faculty_id": {'$addToSet' : "$faculties.facultyGivenId"}}},
    {'$project' :{'_id':0,"faculty_id":1}}
    ])
    return [q for q in query]

def get_academicYear_faculty(facultyGivenId):
    querry = lesson_plan.aggregate([
    {'$match' : {"faculties.facultyGivenId":facultyGivenId}},
    {'$group': { '_id' : 'null',
        "all_academic_year" : {'$addToSet' : "$academicYear"}
        }},
    {'$project' : {'_id' : 0, "all_academic_year":1}}
    ])
    return [q for q in querry]

def  get_terms_faculty(facultyGivenId, academicYear):
    querry = lesson_plan.aggregate([
        { '$match':{
            'faculties.facultyGivenId':facultyGivenId,'academicYear': academicYear 
        }},
        {'$unwind' : '$departments'},
        {'$group' : {'_id' : 'null', 'terms' : {'$addToSet' : '$departments.termNumber'}}},
        {'$project': {'_id':0,'terms':1}}
        ]) 
    return [q for q in querry]


def get_course_of_faculty(facultyGivenId,year,terms):
    courses = lesson_plan.aggregate([
        {"$match":{"academicYear":year,"faculties.facultyGivenId":facultyGivenId,"departments.termNumber":{'$in' :terms}}},
        {'$unwind' : "$faculties" },
        {'$unwind': "$departments"},
        {'$group': {
            '_id':{"courseCode":'$courseCode','coursename':'$courseName','facultyGivenId':'$faculties.facultyGivenId',
            'termNumber':'$departments.termNumber','section':'$departments.section', "facultyName":'$faculties.facultyName',
            'facultyGivenId':'$faculties.facultyGivenId'}
        }},
        {"$project":{
            "courseCode":'$_id.courseCode',"courseName":"$_id.coursename","section":"$_id.section","termNumber":"$_id.termNumber",
         "facultyName":"$_id.facultyName", 'facultyGivenId':'$_id.facultyGivenId' , '_id':0 
         }}
    ])
    codes_info = []
    codes = []
    for course in courses:
        code = course["courseCode"]
        bloom = get_bloomsLevel_Of_Cos(facultyGivenId,year,terms,code)
        if len(bloom) != 0:
            course["Co_details"] = bloom
            codes_info.append(course)
    return codes_info

def get_course_attainment_configuration(year,dept,courseCode):
    attainment_configuration = generic_attainment_configuration.aggregate([
            {"$match":{"academicYear": year,"deptId":dept}},
            {"$unwind":"$courseWiseAttainmentConfiguration"},
            {"$match":{"courseWiseAttainmentConfiguration.courseCode":courseCode}},
            {"$project":{"subGenericAttainmentConfigurationList":1,"courseWiseAttainmentConfiguration":1,"_id":0}}
        ])
    course_attainment_configuration = []
    for attainment in attainment_configuration:
        course_attainment_configuration.append(attainment)
    return course_attainment_configuration
    

def get_course_attainment_information(year,term,courseCode,section,facultyGivenId):
    attainment_data = generic_attainment_data.aggregate([
            {"$unwind":"$courseOutcomeDetailsForAttainment"},
            {"$unwind":"$faculties"},
            {"$match":{"year":year,"termNumber":{"$in":term},"courseDetails.courseCode":courseCode,"section":section,"faculties.facultyGivenId":facultyGivenId}},
            {"$group": {"_id": "null", "uniqueValues": {"$addToSet": "$courseOutcomeDetailsForAttainment"}}},
            {"$project":{"_id":0,"uniqueValues.coNumber":1,"uniqueValues.totalAttainment":1,"uniqueValues.directAttainment":1,"uniqueValues.indirectAttainment":1,"uniqueValues.coTitle":1,}},
        {"$sort": {"uniqueValues.coNumber":1}}])
    course_attainment_data = []
    bloom = get_bloomsLevel_Of_Cos(facultyGivenId,year,term,courseCode)
    for attainment in attainment_data:
        course_attainment_data.append(attainment)
    if len(course_attainment_data) > 0:
        a = course_attainment_data[0]['uniqueValues']
        for i in a:
            for j in bloom:
                if(j.get('CO') == i.get('coNumber')):
                    i["Difficulty"] = j["Difficulty"]
    return course_attainment_data

def get_bloomsLevel_Of_Cos(facultyGivenId, academicYear, term,courseCode):
    blooms = lesson_plan.aggregate([
            {"$unwind":"$faculties"},
            {"$unwind":"$departments"},
            {"$unwind":"$execution"},
            {"$unwind":"$execution.couseOutcomes"},
            {"$match":{"faculties.facultyGivenId":facultyGivenId,"academicYear":academicYear,"departments.termNumber":{'$in' :term},
            "courseCode":courseCode}},
            {"$group":{"_id":{"CO":"$execution.couseOutcomes","Module":"$execution.moduleNumber","Lesson":"$execution.lessonNumber",
            "Topics":"$execution.topicsCovered"}
            ,"blooms":{"$addToSet":"$execution.bloomsLevel"}}},
            {'$sort':{'CO':1}}
        ])
    blooms_level = []
    for bloom in blooms:
        blooms_level.append(bloom)
    CO1 = {}
    CO2 = {}
    CO3 = {}
    CO4 = {}
    CO5 = {}
    CO6 = {}
    for i in blooms_level:
        x = i['_id']
        if(x["CO"] == 1):
            CO1["CO"] = 1
            for x in i['blooms']:
                if(x in CO1):
                    CO1[x] += 1
                else:
                    CO1[x] = 1
        elif(x["CO"] == 2):
            CO2["CO"] = 2
            for x in i['blooms']:
                if(x in CO2):
                    CO2[x] += 1
                else:
                    CO2[x] = 1
        elif(x["CO"] == 3):
            CO3["CO"] = 3
            for x in i['blooms']:
                if(x in CO3):
                    CO3[x] += 1
                else:
                    CO3[x] = 1
        elif(x["CO"] == 4):
            CO4["CO"] = 4
            for x in i['blooms']:
                if(x in CO4):
                    CO4[x] += 1
                else:
                    CO4[x] = 1
        elif(x["CO"] == 5):
            CO5["CO"] = 5
            for x in i['blooms']:
                if(x in CO5):
                    CO5[x] += 1
                else:
                    CO5[x] = 1
        elif(x["CO"] == 6):
            CO6["CO"] = 6
            for x in i['blooms']:
                if(x in CO6):
                    CO6[x] += 1
                else:
                    CO6[x] = 1
    m = difficulty_Of_CO_and_Couse(CO1,CO2,CO3,CO4,CO5,CO6)
    return m

def difficulty_Of_CO_and_Couse(CO1,CO2,CO3,CO4,CO5,CO6):
    diff1 = 0
    diff2 = 0
    diff3 = 0
    diff4 = 0
    diff5 = 0
    diff6 = 0
    for i in CO1:
        if(i == "REMEMBER"):
            diff1 += CO1[i]*1
        elif(i == "UNDERSTAND"):
            diff1 += CO1[i]*2
        elif(i == "APPLY"):
            diff1 += CO1[i]*3
        elif(i == "ANALYZE"):
            diff1 += CO1[i]*4
        elif(i == "EVALUATE"):
            diff1 += CO1[i]*5
        elif(i == "CREATE"):
            diff1 += CO1[i]*6
    for i in CO2:
        if(i == "REMEMBER"):
            diff2 += CO2[i]*1
        elif(i == "UNDERSTAND"):
            diff2 += CO2[i]*2
        elif(i == "APPLY"):
            diff2 += CO2[i]*3
        elif(i == "ANALYZE"):
            diff2 += CO2[i]*4
        elif(i == "EVALUATE"):
            diff2 += CO2[i]*5
        elif(i == "CREATE"):
            diff2 += CO2[i]*6
    for i in CO3:
        if(i == "REMEMBER"):
            diff3 += CO3[i]*1
        elif(i == "UNDERSTAND"):
            diff3 += CO3[i]*2
        elif(i == "APPLY"):
            diff3 += CO3[i]*3
        elif(i == "ANALYZE"):
            diff3 += CO3[i]*4
        elif(i == "EVALUATE"):
            diff3 += CO3[i]*5
        elif(i == "CREATE"):
            diff3 += CO3[i]*6
    for i in CO4:
        if(i == "REMEMBER"):
            diff4 += CO4[i]*1
        elif(i == "UNDERSTAND"):
            diff4 += CO4[i]*2
        elif(i == "APPLY"):
            diff4 += CO4[i]*3
        elif(i == "ANALYZE"):
            diff4 += CO4[i]*4
        elif(i == "EVALUATE"):
            diff4 += CO4[i]*5
        elif(i == "CREATE"):
            diff4 += CO4[i]*6
    for i in CO5:
        if(i == "REMEMBER"):
            diff5 += CO5[i]*1
        elif(i == "UNDERSTAND"):
            diff5 += CO5[i]*2
        elif(i == "APPLY"):
            diff5 += CO5[i]*3
        elif(i == "ANALYZE"):
            diff5 += CO5[i]*4
        elif(i == "EVALUATE"):
            diff5 += CO5[i]*5
        elif(i == "CREATE"):
            diff5 += CO5[i]*6
    for i in CO6:
        if(i == "REMEMBER"):
            diff6 += CO6[i]*1
        elif(i == "UNDERSTAND"):
            diff6 += CO6[i]*2
        elif(i == "APPLY"):
            diff6 += CO6[i]*3
        elif(i == "ANALYZE"):
            diff6 += CO6[i]*4
        elif(i == "EVALUATE"):
            diff6 += CO6[i]*5
        elif(i == "CREATE"):
            diff6 += CO6[i]*6
    CO1["Difficulty"] = diff1
    CO2["Difficulty"] = diff2
    CO3["Difficulty"] = diff3
    CO4["Difficulty"] = diff4
    CO5["Difficulty"] = diff5
    CO6["Difficulty"] = diff6
    return CO1,CO2,CO3,CO4,CO5,CO6

