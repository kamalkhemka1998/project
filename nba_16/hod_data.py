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
    def __init__(self,facultyId,academicYear,termNumber,deptId):
        self.facultyId = facultyId
        self.academicYear = academicYear
        self.termNumber = termNumber
        self.deptId = deptId

def get_user():
    #HOD
    user = User("583","2018-19","6","CS")
    return user

def get_faculty_Ids_of_a_dept():
    user = get_user()
    faculties = lesson_plan.aggregate([
        {
            "$unwind":"$faculties"
        },
        {
            "$unwind":"$departments"
        },
        {
            "$match":{"academicYear":user.academicYear,
                "departments.termNumber":user.termNumber,
                "departments.deptId":user.deptId,
            }
        },
        {
            "$group":{
                "_id":{
                    "courseCode":"$courseCode",
                    "faculty_Id":"$faculties.facultyGivenId",
                    "section":"$departments.section"
                },
                "count":{"$sum":1}
            }
        },
        {
            "$project":{
                "course_code_info":"$_id",
                "_id":0
            }
        }
    ])

    faculties_data = []

    for faculty in faculties:
        faculties_data.append(faculty)

    return faculties_data

def get_cos_of_all_courses_of_a_dept():
    faculties = get_faculty_Ids_of_a_dept()
    user = get_user()
    co_details_of_courses = []
    
    for faculty in faculties:
        course_code_info = faculty['course_code_info']
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
                        "faculties.facultyGivenId":course_code_info['faculty_Id'],
                        "termNumber":user.termNumber,
                        "courseDetails.courseCode":course_code_info['courseCode'],
                        "section":course_code_info['section'],
                        "deptId":user.deptId
                    }
                },
                {
                    "$group":{
                        "_id":{
                            "courseCode":"$courseDetails.courseCode",
                            "section":"$section",
                            "courseName":"$courseDetails.courseName",
                            "courseType":"$courseDetails.courseType",
                            "deptId":"$deptId",
                            "facultyId":"$faculties.facultyGivenId",
                            "facultyName":"$faculties.facultyName"
                        },
                        "average_co_attainments":{"$avg":"$courseOutcomeDetailsForAttainment.totalAttainment"},
                        
                        "co_details":{ "$push":{ "coNumber":"$courseOutcomeDetailsForAttainment.coNumber",
                                                 "coTitle":"$courseOutcomeDetailsForAttainment.coTitle",
                                                 "total_attainment":"$courseOutcomeDetailsForAttainment.totalAttainment",
                                                 "direct_attainment":"$courseOutcomeDetailsForAttainment.directAttainment",
                                                 "indirect_attainment":"$courseOutcomeDetailsForAttainment.indirectAttainment"
                                                 }
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
                        "facultyId":"$_id.facultyId",
                        "facultyName":"$_id.facultyName",
                        "co_details":1,
                        "_id":0 
                    }
                }
            ])
        for co in cos:
            co_details_of_courses.append(co)

    return co_details_of_courses
