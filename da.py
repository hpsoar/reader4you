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

def get_feedlist(user_id):
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

