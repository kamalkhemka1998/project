from pymongo import MongoClient
# from flask_pymongo import PyMongo

db = MongoClient(host='localhost', port = 27017)
mydatabase = db['dhi-mite']
generic_attainment_configuration = mydatabase['dhi_generic_attainment_configuration']
generic_attainment_data = mydatabase['dhi_generic_attainment_data']
lesson_plan = mydatabase['dhi_lesson_plan']
term_detail = mydatabase['dhi_term_detail']
dhi_user = mydatabase['dhi_user']

def get_academicYear_principal():
    querry = lesson_plan.aggregate([ {'$group' : { '_id': 'null',"academicYear" : {'$addToSet' : "$academicYear"} } }  ])
    return [q for q in querry]
    
def get_dept_term_principal(academicYear):
    querry = lesson_plan.aggregate([
            {'$match' : { "academicYear" : academicYear }},
            {'$project' : { "departments.deptId" : 1, "departments.termNumber":1 }},
            {'$unwind' : "$departments"},
            {'$group' : {'_id': 'null', 
                "depts" : {'$addToSet' : "$departments.deptId"},
                "terms" : {'$addToSet' : "$departments.termNumber"}
                }}
        ])
    return [q for q in querry]

def get_dept_hod(employeeGivenId):
    dept_hod = dhi_user.find({'employeeGivenId': employeeGivenId },{'deptId':1})
    return [dept for dept in  dept_hod]

def get_academicYear_hod(dept):
    querry = lesson_plan.aggregate([
    { '$match' : {"faculties.facultyDeptId":'CS'}},
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


def get_course_of_faculty():
    courses = lesson_plan.aggregate([
            {"$unwind":"$faculties"},
            {"$unwind":"$departments"},
            {"$match":{"academicYear":"2018-19","faculties.facultyGivenId":"583","departments.termNumber":"4"}},
            {"$project":{"courseCode":1,"courseName":1,"_id":0}}
        ])
    codes = []
    for course in courses:
        codes.append(course)
    return codes

def get_course_attainment_configuration():
    attainment_configuration = generic_attainment_configuration.aggregate([
            {"$match":{"academicYear":"2018-19","deptId":"CS"}},
            {"$unwind":"$courseWiseAttainmentConfiguration"},
            {"$match":{"courseWiseAttainmentConfiguration.courseCode":"17CS42"}},
            {"$project":{"subGenericAttainmentConfigurationList":1,"courseWiseAttainmentConfiguration":1,"_id":0}}
        ])
    course_attainment_configuration = []
    for attainment in attainment_configuration:
        course_attainment_configuration.append(attainment)
    return course_attainment_configuration
    

def get_course_attainment_information():
    attainment_data = generic_attainment_data.aggregate([
            {"$match":{"year":"2018-19","courseDetails.courseCode":"17CS42","termNumber":"4","section":"A","deptId":"CS"}},
            {"$unwind":"$courseOutcomeDetailsForAttainment"},
            {"$project":{"courseOutcomeDetailsForAttainment.coNumber":1,"courseOutcomeDetailsForAttainment.totalAttainment":1,"courseOutcomeDetailsForAttainment.directAttainment":1,"courseOutcomeDetailsForAttainment.indirectAttainment":1,"_id":0}}
        ])
    course_attainment_data = []
    for attainment in attainment_data:
        course_attainment_data.append(attainment)
    return course_attainment_data

