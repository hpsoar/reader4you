
"""
  Data Access Module
  ~~~~~~~~~~~~~~~~~~

  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
from pymongo import Connection

host = '127.0.0.1'
_connection = Connection(host, 27017)
db = _connection['FEED4YOU-db']

def gen_id(key_str):
  result = db.ids.find_and_modify(query={'key':key_str}, update={'$inc':{'id':1}}, upsert=True)
  if not result:
    result = db.ids.find_and_modify(query={'key':key_str}, update={'$inc':{'id':10000000}}, upsert=True)
  return result['id']

def save_feed(feed):
  db.feeds.save(feed)

def get_all_feeds();
  return list(db.feeds.find_all())

def get_feedlist_for_user(user_id):
  return list(db.feeds.find({'user_id': user_id}))

def save_article(article):
  db.articles.save(article)

def get_articles(feed_id):
  return list(db.articles.find({'feed_id': int(feed_id)}))

def get_feed(feed_id):
  return db.feeds.find_one({'id': int(feed_id) })

def get_feed_id(user_id, url):
  feed = db.feeds.find_one({'user_id': user_id, 'url': url})
  if feed: return ['id']
  else: return None

def get_article(feed_id, link):
  return db.articles.find_one({'feed_id': int(feed_id), 'link': link})

class Story:
  feed_id = -1
  title = ''
  summary = ''
  author = ''
  publish_date = '' # TODO: remove this
  publish_date = datetime.datetime.utcnow()
  link = ''
  guid = ''
  story_class = -1
  tags = []

  @classmethod
  def filter(cls, **kwargs):
    pass

class Feed:
  title = ''
  description = ''
  address = ''
  link = ''

  @classmethod
  def filter(cls, **kwargs):
    pass

  @classmethod
  def get_or_create(cls, address):
    pass

  @classmethod
  def get_by_url(cls, url):
    pass

class Subscription:
  user_id = -1
  feed_id = -1
  active = False
  unread_count = 0
  last_read_date = datetime.datetime.utcnow()

  @classmethod
  def get_by_user(user_id):
    pass

  def get_by_feed(feed_id):
    pass

