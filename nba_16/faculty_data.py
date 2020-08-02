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

def get_co_methods():
    academicYear = "2018-19"
    facultyGivenId = "67"
    termNumber = "7"
    section = "A"
    courseCode = "15IM71"
    coNumber = 1

    coDetails = generic_attainment_data.aggregate( [ 
        { "$unwind" : "$faculties" } ,
        { "$unwind" : "$courseOutcomeDetailsForAttainment" },
        { "$match" : {
            "academicYear" : academicYear,
            "faculties.facultyGivenId" : facultyGivenId,
            "termNumber" : termNumber,
            "section" : section,
            "courseDetails.courseCode" : courseCode,
            "courseOutcomeDetailsForAttainment.coNumber" : coNumber
            } 
        },
        { "$project" : {
            "facultyId" : "$faculties.facultyGivenId",
            "facultyName" : "$faculties.facultyName",
            "courseCode" : "$courseDetails.courseCode",
            "courseName" : "$courseDetails.courseName",
            "coNumber" : "$courseOutcomeDetailsForAttainment.coNumber",
            "directMethods" : "$courseOutcomeDetailsForAttainment.directMethods",
            "indirectMethods" : "$courseOutcomeDetailsForAttainment.indirectMethods",
            "_id" : 0
            } 
        }
        ] )
    
    co_methods = []    

    for field in coDetails:
        co_methods.append([field])
      
    co_methods=co_methods[0]

    return co_methods

def get_co_data():
    m = get_co_methods()
    test_co_details = {}
    directMethods = []
   
    directMethods = m[0]['directMethods']
    indirectMethods = m[0]['indirectMethods']

    test_co_details['courseCode'] = m[0]['courseCode']
    test_co_details['courseName'] = m[0]['courseName']
    test_co_details['facultyId'] = m[0]['facultyId']
    test_co_details['facultyName'] = m[0]['facultyName']
    test_co_details['direct_attainment_details'] = []
    test_co_details['indirect_attainment_details'] = []
   
    w = get_weightage()
    f = w[0]['firstLevelWeightage']
    test_co_details['directAttainmentWeightage'] = f['directMethodWeightage']
    test_co_details['indirectAttainmentWeightage'] = f['indirectMethodWeightage']

    for method in directMethods:
        if method['methodName'] == "IA":
            method_details = method['nextLevelAttainments']
        
        elif method['methodName'] == "Other Assessment":
            sub = []
            sub = method['subAssessmentMethods']
            method_details = sub[0]['nextLevelAttainments']
      
        else:
            sub = []
            sub.append({
                "numberOfStudentsParticipated" : method['numberOfStudentsParticipated'],
                "numberOfTargetAttainedStudents" : method['numberOfTargetAttainedStudents']
            })
            method_details = sub

        test_co_details['direct_attainment_details'].append({
            "methodName" : method['methodName'],
            "description" : method['methodDescription'],
            "attainment" : method['attainment'],
            "attainmentPercentage" : method['attainmentPercentage'],
            "method_details" : method_details
            })

    for method in indirectMethods:
        test_co_details['indirect_attainment_details'].append({
            "methodName" : method['methodName'],
            "description" : method['methodDescription'],
            "attainment" : method['attainment'],
            "attainmentPercentage" : method['attainmentPercentage']
            })
    
    return test_co_details
    
def get_weightage():
    academicYear = "2018-19"
    deptId = "IS"
    courseType = "THEORY"
    weightage = generic_attainment_configuration.aggregate([
        {"$unwind":"$subGenericAttainmentConfigurationList"},
        {
            "$match":{
                "academicYear":academicYear,
                "deptId" : deptId,
                "subGenericAttainmentConfigurationList.courseType":courseType
            }
        },
        {
            "$project":{
                "firstLevelWeightage" : "$subGenericAttainmentConfigurationList.firstLevelWeightage",
                "_id" : 0
                }
        }
            
    ])
    
    weightages = []

    for w in weightage:
        weightages.append(w)
    return weightages