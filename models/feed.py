
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
  story_id = -1
  feed_id = -1
  title = ''
  summary = ''
  author = ''
  #publish_date = '' # TODO: remove this
  publish_date = datetime.datetime.utcnow()
  link = ''
  uuid = ''
  story_class = -1
  tags = []

  def __init__(self, feed_id):
    self.feed_id = feed_id
    self.story_id = gen_id('stories')

  @classmethod
  def filter(cls, **kwargs):
    pass

FEED_OK, FEED_SAME, FEED_ERRHTTP, FEED_ERRPARSE = range(3)

class ProcessFeed:
    def __init__(self, feed, fpf, options):
        self.feed = feed
        self.options = options
        self.fpf = fpf
    
    def process(self):
        """ Downloads and parses a feed.
        """
        start = time.time()

        ret_values = dict(new=0, updated=0, same=0, error=0)

        if hasattr(self.fpf, 'status'):
            if self.fpf.status == 304:
                # TODO: self.feed.save_feed_history(304, "Not modified")
                return FEED_SAME, ret_values
            
            if self.fpf.status in (302, 301):
                if not self.fpf.href.endswith('feedburner.com/atom.xml'):
                    self.feed.feed_address = self.fpf.href
                if not self.feed.known_good:
                    print 'TODO: schedule for anothrer fetch'
                if not self.fpf.entries:
                    self.feed = self.feed.save()
                    #self.feed.save_feed_history(self.fpf.status, "HTTP Redirect")
                    return FEED_ERRHTTP, ret_values
            if self.fpf.status >= 400:
              # TODO: process error
              return FEED_ERRHTTP, ret_values

        if not self.fpf.entries:
            if self.fpf.bozo and isinstance(self.fpf.bozo_exception, feedparser.NonXMLContentType):
                # TODO: process error
                return FEED_ERRPARSE, ret_values
            elif self.fpf.bozo and isinstance(self.fpf.bozo_exception, xml.sax._exceptions.SAXException):
                # TODO: process error
                return FEED_ERRPARSE, ret_values
                
        # the feed has changed (or it is the first time we parse it)
        # saving the etag and last_modified fields
        self.feed.etag = self.fpf.get('etag')
        if self.feed.etag:
            self.feed.etag = self.feed.etag[:255]
        # some times this is None (it never should) *sigh*
        if self.feed.etag is None:
            self.feed.etag = ''

        try:
            self.feed.last_modified = mtime(self.fpf.modified)
        except:
            self.feed.last_modified = None
        
        self.fpf.entries = self.fpf.entries[:50] #TODO
        
        if self.fpf.feed.get('title'):
            self.feed.feed_title = self.fpf.feed.get('title')

        tagline = self.fpf.feed.get('tagline', self.feed.data.feed_tagline)
        if tagline:
            # TODO: save?
            print 'tagline: %s' % tagline

        if not self.feed.feed_link_locked:
            self.feed.feed_link = self.fpf.feed.get('link') or self.fpf.feed.get('id') or self.feed.feed_link
        
        self.feed = self.feed.save()

        # Compare new stories to existing stories, adding and updating
        for e in self.fpf.entries:
          story = Story(self.feed.feed_id)
          story.summary = e.get('summary') or e.get('description')
          story.title = e.get('title')
          story.author = e.get('author')
          story.link = e.get('link')
          story.uuid = e.get('uuid')
          for tag in e.tags:
            # TODO add to story.tags
            print tag

          if e.get('published_parsed'): story.publish_date = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed))

        return FEED_OK, ret_values

class FetchFeed:
  def __init__(self, feed):
    self.feed = feed

  def fetch(self, force=False):
    etag = self.feed.etag
    modified = self.feed.last_modified
    address = self.feed.address
    if force:
      etag = None
      modified = None

    USER_AGENT = 'NewsBlur Feed Fetcher - %s subscriber%s - %s (Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.2.3 (KHTML, like Gecko) Version/5.2)' % (
            self.feed.num_subscribers,
            's' if self.feed.num_subscribers > 1 else '',
            settings.READER4YOU_URL
        )
    try:
      fpfeed = feedparser.parse(address,
                                agent=USER_AGENT,
                                etag=etag,
                                modified=modified))
    except (TypeError, ValueError), e:
      feedparser.PARSE_MICROFORMATS = False
      fpfeed = feedparser.parse(address,
                                agent=USER_AGENT,
                                etag=etag,
                                modified=modified))
      feedparser.PARSE_MICROFORMATS = True
    return fpfeed

  def process(fetched_feed):
       
    return feed

class Feed:
  feed_id = -1
  feed_title = ''
  feed_address = ''
  feed_link = ''
  feed_link_locked = False
  description = ''
  num_subscribers = 0
  etag = None
  last_modified = None
  tags = []

  def __init__(self, address):
    self.feed_id = gen_id('feeds')
    self.address = address

  def save(self):
    db.save({
      '_id': feed_id,
      })

  def update(self, force=False):
    ffeed = FetchFeed(self)
    fetched_feed = ffeed.fetch(force)
    pfeed = ProcessFeed(self, fetched_feed)
    ret, feed = pfeed.process()

    if ret == FEED_OK: return feed
    return self

  @classmethod
  def filter(cls, **kwargs):
    return list(db.feeds.find(**kwargs))

  @classmethod
  def get_or_create(cls, address):
    feed = cls.get_by_url(address)
    if feed: return feed

    return Feed(address).update()

  @classmethod
  def get_by_url(cls, url):
    feeds = cls.filter({'address': url})
    if feeds and len(feeds) > 0: return feeds[0]
    feeds = cls.filter({'link': url})
    if feeds and len(feeds) > 0: return feeds[0]
    return None

  @classmethod
  def get_all_feed(cls):
    return db.feeds.find({})

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

