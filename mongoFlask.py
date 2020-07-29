from bson import ObjectId
from flask.json import JSONEncoder

class MongoJSON_Encoder(JSONEncoder):
    def default(self,o):
        if isinstance(o,ObjectId):
            return str(o)