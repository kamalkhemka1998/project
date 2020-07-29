from pymongo import MongoClient
from pprint import pprint

db = MongoClient('localhost',27017)

mydb = db['dhi-mite']

users = mydb['dhi_user']
term_detail = mydb['dhi_term_detail']
lesson_plan = mydb['dhi_lesson_plan']
generic_attainment_configuration = mydb['dhi_generic_attainment_config']
generic_attainment_data = mydb['dhi_generic_attainment_data']

def get_course_code():
    courses = lesson_plan.aggregate([
        {
            "$unwind":"$faculties"
        },
        {
            "$unwind":"$departments"
        },
        {
            "$match":{"academicYear":"2018-19",
                "faculties.facultyGivenId":"172",
                "departments.termNumber":"3"
            }
        },
        {
            "$project":{"courseCode":1,
                "_id":0
            }
        }
        ])
    
    course_codes = []

    for course in courses:
        course_codes.append(course)
    
    return course_codes

def get_cos_of_courses():
    cos = generic_attainment_data.aggregate([
            {
                "$unwind":"$faculties"
            },
            {
                "$unwind":"$courseOutcomeDetailsForAttainment"
            },
            {
                "$match":{"academicYear":"2018-19",
                    "faculties.facultyGivenId":"172",
                    "termNumber":"3",
                    "courseDetails.courseCode":"17CS36"
                }
            },
            {
                "$project":{"coNumber":"$courseOutcomeDetailsForAttainment.coNumber",
                    "total_attainment":"$courseOutcomeDetailsForAttainment.totalAttainment",
                    "courseCode":"$courseDetails.courseCode",
                    "section":1,
                    "_id":0
                }
            }
        ])
    
    co_details = []

    for co in cos:
        co_details.append(co)
    
    return co_details

