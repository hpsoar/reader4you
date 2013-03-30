"""
  Feed Engine
  ~~~~~~~~~~~~

  a module manages feeds & articles

  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
import da
from tools import jsonify
import urllib2
import feedparser

def default_rss(url):
  feed = { }
  feed['title'] = ''
  feed['description'] = ''
  feed['link'] = ''
  feed['language'] = ''
  feed['url'] = url
  return feed

def default_item():
  item = { }
  item['title'] = ''
  item['description'] = ''
  item['author'] = ''
  item['pubDate'] = ''
  #item['title_features'] = { }
  #item['description_features'] = { }
  item['link'] = ''
  item['guid'] = ''
  return item

def parse_article(e):
  item = default_item()
  item['title'] = e.title

  if 'summary' in e: item['description'] = e.summary
  else: item['description'] = e.description

  if 'author' in e: item['author'] = e.author
  if 'pubDate' in e: item['pubDate'] = e.pubDate
  if 'link' in e: item['link'] = e.link
  if 'guid' in e: item['guid'] = e.guid
  #item['title_features'] = extract_features(item['title'])
  #item['description_features'] = extract_features(item['description'])
  return item

def parse_feed(url):
  try:
    content = urllib2.urlopen(url, timeout=2).read()
  except:
    return None, None

  d = feedparser.parse(content)
  print d.feed

  feed = default_rss(url)
  feed['title'] = d.feed.title
  if 'link' in d.feed: feed['link'] = d.feed.link
  if 'language' in d.feed: feed['language'] = d.feed.language

  if 'summary' in d.feed: feed['description'] = d.feed.summary
  else: feed['description'] = d.feed.description

  articles = [parse_article(e) for e in d.entries]
  return feed, articles


def add_feed(user_id, url):
  feed, articles = parse_feed(url)

  if feed:
    feed['user_id'] = user_id
    feed['id'] = da.gen_id('feeds')

    da.save_feed(feed)

    for item in articles:
      item['id'] = da.gen_id('articles')
      item['feed_id'] = feed['id']
      da.save_article(item)
    
    # append articles
    feed['articles'] = articles
  return jsonify(feed)

def get_feedlist(user_id):
  feedlist = da.get_feedlist(user_id)
  articles = []
  if feedlist: articles = da.get_articles(feedlist[0]['id'])

  return jsonify({ 'feedlist': feedlist, 'articles': articles})

def get_articles(feed_id):
  return jsonify({ 'articles': da.get_articles(feed_id) })

