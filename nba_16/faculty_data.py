from pymongo import MongoClient
from pprint import pprint

db = MongoClient('localhost',27017)

mydb = db['dhi-mite']

users = mydb['dhi_user']
term_detail = mydb['dhi_term_detail']
lesson_plan = mydb['dhi_lesson_plan']
generic_attainment_configuration = mydb['dhi_generic_attainment_config']
generic_attainment_data = mydb['dhi_generic_attainment_data']

class User:
    def __init__(self,facultyId,academicYear,termNumber):
        self.facultyId = facultyId
        self.academicYear = academicYear
        self.termNumber = termNumber

def get_user():
    #Faculty
    user = User("67","2018-19","6")
    return user

def get_course_code(facultyId,academicYear,termNumber):
    courses = lesson_plan.aggregate([
        {
            "$unwind":"$faculties"
        },
        {
            "$unwind":"$departments"
        },
        {
            "$match":{"academicYear":academicYear,
                "faculties.facultyGivenId":facultyId,
                "departments.termNumber":termNumber
            }
        },
        {
            "$project":{"courseCode":1,
                "section":"$departments.section",
                "_id":0
            }
        }
        ])
    
    course_codes = []

    for course in courses:
        course_codes.append(course)
    
    return course_codes

def get_cos_of_courses(course_codes,facultyId,academicYear,termNumber):
    co_details_of_courses = []
    for course_code in course_codes:
        cos = generic_attainment_data.aggregate([
                {
                    "$unwind":"$faculties"
                },
                {
                    "$unwind":"$courseOutcomeDetailsForAttainment"
                },
                {
                    "$match":
                    {
                        "year":academicYear,
                        "faculties.facultyGivenId":facultyId,
                        "termNumber":termNumber,
                        "courseDetails.courseCode":course_code['courseCode'],
                        "section":course_code['section']
                    }
                },
                {
                    "$group":{
                        "_id":{
                            "courseCode":"$courseDetails.courseCode",
                            "section":"$section",
                            "courseName":"$courseDetails.courseName",
                            "courseType":"$courseDetails.courseType",
                            "deptId":"$deptid"
                        },
                        "average_co_attainments":{"$avg":"$courseOutcomeDetailsForAttainment.totalAttainment"},
                        
                        "co_details":{ "$push":{ "coNumber":"$courseOutcomeDetailsForAttainment.coNumber",
                                                 "coTitle":"$courseOutcomeDetailsForAttainment.coTitle",
                                                 "total_attainment":"$courseOutcomeDetailsForAttainment.totalAttainment",
                                                 "direct_attainment":"$courseOutcomeDetailsForAttainment.directAttainment",
                                                 "indirect_attainment":"$courseOutcomeDetailsForAttainment.indirectAttainment"}
                                             }
                                             
                    }
                },
                {
                    "$project":
                    {
                        "average_co_attainments":1,
                        "courseCode":"$_id.courseCode",
                        "section":"$_id.section",
                        "courseName":"$_id.courseName",
                        "courseType":"$_id.courseType",
                        "deptId":"$_id.deptId",
                        "co_details":1,
                        "_id":0
                    }
                }
            ])
        for co in cos:
            co_details_of_courses.append(co)

    return co_details_of_courses

def get_rubrics_details(academicYear,deptId,courseType):
    rubrics = generic_attainment_configuration.aggregate([
        {
            "$unwind":"$subGenericAttainmentConfigurationList"
        },
        {
            "$match":{
                "academicYear":academicYear,
                "subGenericAttainmentConfigurationList.courseType":courseType,
                "deptId":deptId
            }
        },
        {
            "$project":{
                "subGenericAttainmentConfigurationList.directMethods.rubricDetail":1,
                "subGenericAttainmentConfigurationList.directMethods.methodName":1,
                "subGenericAttainmentConfigurationList.directMethods.methodName":1,
                "subGenericAttainmentConfigurationList.indirectMethods.rubricDetail":1,
                "_id":0
            }
        }

        ])

    rubric_details = []
    for rubric in rubrics:
        rubric_details.append(rubric)

    return rubric_details