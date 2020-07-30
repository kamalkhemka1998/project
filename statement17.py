from pymongo import MongoClient
from flask_pymongo import PyMongo

db = MongoClient(host='localhost', port = 27017)
mydatabase = db['nba-analytics-backend']
generic_attainment_configuration = mydatabase['dhi_generic_attainment_configuration']
generic_attainment_data = mydatabase['dhi_generic_attainment_data']
lesson_plan = mydatabase['dhi_lesson_plan']
term_detail = mydatabase['dhi_term_detail']

def get_terms_details(): 
    results =  mydatabase.term_detail.find({})
    data = []
    for res in results:
        data.append(res)
        print(res)
    return data

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

