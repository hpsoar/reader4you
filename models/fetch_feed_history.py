import feedparser
import urllib, datetime
from models.feed import Feed
from models.da import DBObject, db
from models.util_feed import ProcessFeed
import threading
from juggernaut import Juggernaut

jug = Juggernaut()

class FetchedFeed(DBObject):
  def __init__(self, feed_id):
    self.feed_id = feed_id

  def save(self):
    db.loaded_feeds.save(self.__dict__)

  #TODO: put into DBObject
  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.loaded_feeds.find(query)]

  @classmethod
  def get_by_id(cls, feed_id):
    feeds = cls.filter({'feed_id':feed_id})
    if feeds and len(feeds) > 0: return feeds[0]
    return None

class HistoryStoryFetcher(threading.Thread):
  def __init__(self, max_n=200):
    threading.Thread.__init__(self)
    self.queue = []
    self.max_n = max_n

  def add_feed(self, feed_id):
    feed_id = int(feed_id)
    #feed = Feed.get_by_id(feed_id)
    #if feed and not 
    if not feed_id in self.queue:
      self.queue.append(feed_id)
      return True
    return False

  def add_feeds(self, feed_ids):
    """
    return a list of state for each feed
    """
    return [self.add_feed(feed_id) for feed_id in feed_ids]

  def run(self):
    self.process()

  def process(self):
    while len(self.queue) > 0:
      feed_id = self.queue[0]
      self.queue = self.queue[1:]
      self.fetch_feed(feed_id)

  def fetch_feed(self, feed_id):
    feed = Feed.get_by_id(feed_id)
    if not feed: return

    url = ('https://www.google.com/reader/public/atom/feed/%s?n=%d' % 
        (feed.feed_address, self.max_n))
    try:
      fetched_feed = feedparser.parse(url)
  
      FetchedFeed(feed_id).save()
      
      pfeed = ProcessFeed(feed, fetched_feed, {});

      ret, feed = pfeed.process()

      jug.publish('import:google-reader-history', {'state':'ok', 'feed_id': feed_id })
    except Exception, e:
      print e
      jug.publish('import:google-reader-history', {'state':'error', 'feed_id':feed_id})


