from da import db, gen_id, DBObject

class User(DBObject):
  def __init__(self, username='', password=''):
    self._id = gen_id('users')
    self.username = username
    self.password = password
  
  @property
  def user_id(self):
    return self._id

  def save(self):
    db.users.save(self.__dict__)

  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.users.find(query)]

  @classmethod
  def get_by_name(cls, username):
    users = cls.filter({'username': username})
    if users and len(users) > 0: return users[0]
    return None

  @classmethod
  def get_by_id(cls, user_id):
    users = cls.filter({'_id': int(user_id) })
    if users and len(users) > 0: return users[0]
    return None


