import datetime
import settings
import feedparser
import time
import xml
from feed import Feed, Story

FEED_OK, FEED_SAME, FEED_ERRHTTP, FEED_ERRPARSE = range(4)

class ProcessFeed:
  def __init__(self, feed, fpf, options):
    self.feed = feed
    self.fpf = fpf
    self.options = options
  
  def process(self):
    if hasattr(self.fpf, 'status'):
      if self.fpf.status == 304:
        # TODO: self.feed.save_feed_history(304, "Not modified")
        return FEED_SAME, self.feed
      
      if self.fpf.status in (302, 301):
        if not self.fpf.href.endswith('feedburner.com/atom.xml'):
          self.feed.feed_address = self.fpf.href
          # TODO: this may lead to duplicate feed

        #if not self.feed.known_good:
        #  print 'TODO: schedule for anothrer fetch'
        if not self.fpf.entries:
          #self.feed.save_feed_history(self.fpf.status, "HTTP Redirect")
          self.feed.save()
          return FEED_ERRHTTP, self.feed
      if self.fpf.status >= 400:
        # TODO: process error
        return FEED_ERRHTTP, self.feed

    if not self.fpf.entries:
      if self.fpf.bozo and isinstance(self.fpf.bozo_exception, feedparser.NonXMLContentType):
        # TODO: process error
        return FEED_ERRPARSE, self.feed
      elif self.fpf.bozo and isinstance(self.fpf.bozo_exception, xml.sax._exceptions.SAXException):
        # TODO: process error
        return FEED_ERRPARSE, self.feed
            
    # the feed has changed (or it is the first time we parse it)
    # saving the etag and last_modified fields
    self.feed.etag = self.fpf.get('etag')

    if self.feed.etag: self.feed.etag = self.feed.etag[:255]

    # some times this is None (it never should) *sigh*
    if self.feed.etag is None: self.feed.etag = ''

    try:
      self.feed.last_modified = mtime(self.fpf.modified)
    except:
      self.feed.last_modified = None
    
    self.fpf.entries = self.fpf.entries[:50] #TODO
    
    if self.fpf.feed.get('title'):
      self.feed.feed_title = self.fpf.feed.get('title')

    tagline = self.fpf.feed.get('tagline', self.feed.feed_tagline)
    if tagline:
      # TODO: save?
      print 'tagline: %s' % tagline

    if not self.feed.feed_link_locked:
      self.feed.feed_link = self.fpf.feed.get('link') or self.fpf.feed.get('id') or self.feed.feed_link
    
    self.feed.save()

    # Compare new stories to existing stories, adding and updating
    for e in self.fpf.entries:
      link = e.get('link') or e.get('id') or story.link
      if not link: continue
      story, exist = Story.get_or_create(self.feed.feed_id, link)
      if exist: continue

      story.summary = e.get('summary') or e.get('description') or story.summary
      story.title = e.get('title')
      story.author = e.get('author') or story.author
      story.link = link
      for tag in e.get('tags') or []:
        # TODO add to story.tags
        print tag

      if e.get('published_parsed'): story.publish_date = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed))
      story.save()

    return FEED_OK, self.feed

class FetchFeed:
  def __init__(self, feed):
    self.feed = feed

  def fetch(self, force=False):
    etag = self.feed.etag
    modified = self.feed.last_modified
    address = self.feed.feed_address
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
                                modified=modified)
    except (TypeError, ValueError), e:
      feedparser.PARSE_MICROFORMATS = False
      fpfeed = feedparser.parse(address,
                                agent=USER_AGENT,
                                etag=etag,
                                modified=modified)
      feedparser.PARSE_MICROFORMATS = True
    return fpfeed
