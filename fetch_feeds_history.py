import feedparser
import urllib, datetime
import da

class FetchedFeed:
  @classmethod
  def add_feed(cls, url):
    cls.db().save({
      'url' : url,
      'update_time' : datetime.dateime.utcnow(),
      })

  @classmethod
  def get_by_url(cls, url):
    return cls.db().find_one({'url': url})

  @classmethod
  def db(cls):
    return da.history_fetched_feeds

def fetch_feed(feed_url, n):
  # TODO: call google
  url = ('http://www.google.com/reader/public/atom/feed/%s?n=%d' % 
      (urllib.quote(feed_url), n))
  feed = feedparser.parse(url)

  for e in feed.entries:
    if 'title' in e: print e['title']

  FetchedFeed.add_feed(feed_url)


def fetch(force=False, n=99999):
  for feed in da.get_all_feeds():
    url = feed['url']
    if force:
      fetch_feed(url, n)
    elif not FetchedFeed.get_by_url(url):
      fetch_feed(url, n)
  
