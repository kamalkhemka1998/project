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

    '''HOD
    user = User("583")'''

    return user

def get_course_code():
    user = get_user()
    courses = lesson_plan.aggregate([
        {
            "$unwind":"$faculties"
        },
        {
            "$unwind":"$departments"
        },
        {
            "$match":{"academicYear":user.academicYear,
                "faculties.facultyGivenId":user.facultyId,
                "departments.termNumber":user.termNumber
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

def get_cos_of_courses(course_codes):
    user = get_user()
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
                        "year":user.academicYear,
                        "faculties.facultyGivenId":user.facultyId,
                        "termNumber":user.termNumber,
                        "courseDetails.courseCode":course_code['courseCode'],
                        "section":course_code['section']
                    }
                },
                {
                    "$project":
                    {
                        "coNumber":"$courseOutcomeDetailsForAttainment.coNumber",
                        "total_attainment":"$courseOutcomeDetailsForAttainment.totalAttainment",
                        "direct_attainment":"$courseOutcomeDetailsForAttainment.directAttainment",
                        "indirect_attainment":"$courseOutcomeDetailsForAttainment.indirectAttainment",
                        "courseCode":"$courseDetails.courseCode",
                        "courseName":"$courseDetails.courseName",
                        "courseType":"$courseDetails.courseType",
                        "deptId":1,
                        "section":1,
                        "_id":0
                    }
                }
            ])

        x = []
        total_attainment = index = avg_attainment = 0
        for co in cos:
            x.append(co)
            total_attainment += x[index]['total_attainment']
            index += 1
        average_attainment = total_attainment/index
        co_details_of_courses.append({"average_attainment_cos":average_attainment,"course_outcomes_of_particular_course":x})


    return co_details_of_courses
