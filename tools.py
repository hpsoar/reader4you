import datetime
from models.da import DBObject

try:
    import json
except ImportError:
    import simplejson as json

try:
    from bson.objectid import ObjectId
except:
    pass


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.ctime()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, DBObject):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def jsonify(data):
    return json.dumps(data, cls=APIEncoder)
