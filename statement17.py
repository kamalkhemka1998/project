from pymongo import MongoClient
from flask import jsonify
from flask_pymongo import PyMongo

db = MongoClient(host='localhost', port = 27017)
mydatabase = db['analytics']
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