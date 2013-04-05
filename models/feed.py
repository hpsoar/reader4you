
"""
  Data Access Module
  ~~~~~~~~~~~~~~~~~~

  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
import datetime
from da import db, gen_id, DBObject
import utils.urlnorm as urlnorm

class Story(DBObject):
  def __init__(self, feed_id=-1, link=''):
    self.feed_id = feed_id
    self.link = link and urlnorm.normalize(link)

    self.story_id = gen_id('stories')
    self.title = ''
    self.summary = ''
    self.author = ''
    #publish_date = '' # TODO: remove this
    self.publish_date = datetime.datetime.utcnow()
    self.story_class = -1

  def save(self):
    db.stories.save(self.__dict__)

  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.stories.find(query)]

  @classmethod
  def get_stories_for_feed(cls, feed_id):
    return cls.filter({'feed_id': int(feed_id)})

  @classmethod
  def get_all_stories(cls):
    return cls.filter({})

  @classmethod
  def get_or_create(cls, feed_id, link):
    stories = cls.filter({'feed_id': feed_id, 'link': link})
    if stories and len(stories) > 0: return stories[0], True
    return Story(feed_id, link), False

  @classmethod
  def get_by_id(cls, story_id):
    stories = cls.filter({'story_id': story_id})
    if stories and len(stories) > 0: return stories[0]
    return None

class Feed(DBObject):
  def __init__(self, address='', title='', link=''):
    self.feed_id = gen_id('feeds')
    self.feed_address = address
    self.feed_title = title
    self.feed_link = link
    self.feed_link_locked = False
    self.feed_tagline = ''
    self.description = ''
    self.num_subscribers = 0
    self.etag = None
    self.last_modified = None

  def save(self):
    db.feeds.save(self.__dict__)

  def update(self, force=False):
    from util_feed import FetchFeed, ProcessFeed

    ffeed = FetchFeed(self)
    fetched_feed = ffeed.fetch(force)
    pfeed = ProcessFeed(self, fetched_feed, {})
    ret, feed = pfeed.process()

    return feed

  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.feeds.find(query)]

  @classmethod
  def get_or_create(cls, address, title='', link=''):
    address = urlnorm.normalize(address)
    link = link and urlnorm.normalize(link)

    feed = cls.get_by_url(address)
    if feed: return feed, True
    feed = Feed(address, title = title, link = link)
    feed.save()
    return feed.update(), False

  @classmethod
  def get_by_url(cls, url):
    url = urlnorm.normalize(url)
    feeds = cls.filter({'feed_address': url})
    if feeds and len(feeds) > 0: return feeds[0]
    feeds = cls.filter({'feed_link': url})
    if feeds and len(feeds) > 0: return feeds[0]
    return None

  @classmethod
  def get_all_feeds(cls):
    return cls.filter({})

  @classmethod
  def get_by_id(cls, feed_id):
    feeds = cls.filter({'feed_id': int(feed_id)})
    if feeds and len(feeds) > 0: return feeds[0]
    return None
  
class Subscription(DBObject):
  def __init__(self, user_id=-1, feed_id=-1):
    self.sub_id = gen_id('subscriptions')
    self.user_id = user_id
    self.feed_id = feed_id
    self.active = False
    self.unread_count = 0
    self.last_read_date = datetime.datetime.utcnow()

  def save(self):
    db.subscriptions.save(self.__dict__)

  @classmethod
  def filter(cls, query):
    return [cls.dict2obj(cur) for cur in db.subscriptions.find(query)]

  @classmethod
  def get_by_user(cls, user_id):
    return cls.filter({'user_id': int(user_id)})

  @classmethod
  def get_by_feed(cls, feed_id):
    return Subscription.filter({'feed_id': int(feed_id)})
  
  @classmethod
  def get_subscription(cls, user_id, feed_id):
    subs = cls.filter({'feed_id': int(feed_id), 'user_id': int(user_id) })
    if subs and len(subs) > 0: return subs[0]
    return None

  @classmethod
  def get_or_create(cls, user_id, feed_id):
    sub = cls.get_subscription(user_id, feed_id)
    if sub: return sub, True
    sub = Subscription(user_id, feed_id)
    sub.save()
    return sub, False

