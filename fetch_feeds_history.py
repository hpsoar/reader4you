import feedparser
import urllib, datetime
from models.feed import Feed
from models.da import DBObject

class FetchedFeed(DBObject):
  def __init__(self, feed_id):
    self.feed_id = feed_id

  def save(self):
    self.loaded_feeds.save(self.__dict__)

  #TODO: put into DBObject
  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.loaded_feeds.find(query)]

  @classmethod
  def get_by_id(cls, feed_id):
    feeds = cls.filter({'feed_id':feed_id})
    if feeds and len(feeds) > 0: return feeds[0]
    return None

class HistoryStoryFetcher:
  def __init__(self, max_n=9999):
    self.queue = []
    self.max_n = max_n

  def add_feed(self, feed_id):
    feed = Feed.get_by_id(feed_id)
    if feed and not FetchedFeed.get_by_id(feed.feed_id):
      self.queue.append({
        'id': feed.feed_id,
        'address': feed.feed_address,
        })

  def add_feeds(self, feed_ids):
    for feed_id in feed_ids:
      self.add_feed(feed_id)

  def process(self):
    while len(self.queue) > 0:
      feed = self.queue[0]
      self.queue = self.queue[1:]
      self.fetch(feed)

  def fetch_feed(self, feed):
    # TODO: call google
    url = ('http://www.google.com/reader/public/atom/feed/%s?n=%d' % 
        (urllib.quote(feed['address']), self.max_n))

    fetched_feed = feedparser.parse(url)
  
    FetchedFeed(feed['id']).save()

