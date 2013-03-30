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
import time
import datetime

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
  item['published'] = ''
  item['published_parsed'] = datetime.datetime.utcnow()
  #item['title_features'] = { }
  #item['description_features'] = { }
  item['link'] = ''
  item['guid'] = ''
  return item

def parse_article(e):
  item = default_item()

  if 'summary' in e: item['description'] = e.summary
  else: item['description'] = e.description

  if 'published_parsed' in e: item['published_parsed'] = datetime.datetime.fromtimestamp(time.mktime(e.published_parsed))

  for key in item.keys():
    if key == 'description' or key == 'published_parsed': continue
    if key in e: item[key] = e[key]

  #print e.published_parsed
  #item['title'] = e.title
  #if 'author' in e: item['author'] = e.author
  #if 'created' in e: item['created'] = e.created
  #if 'pubDate' in e: item['pubDate'] = e.pubDate
  #if 'link' in e: item['link'] = e.link
  #if 'guid' in e: item['guid'] = e.guid
  #item['title_features'] = extract_features(item['title'])
  #item['description_features'] = extract_features(item['description'])
  return item

def read(url):
  try:
    return urllib2.urlopen(url, timeout=2).read()
  except:
    return None

def parse_feed(url, content):
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
  """
  add feed for user

  return: @state 'ok'/'network error'/'duplication'
          @feed feed information
          @articles latested articles
  """
  state = 'ok'
  if da.get_feed_id(user_id, url):
    state = 'duplication'
    return jsonify({'state': state})

  content = read(url)
  if not content:
    state = 'network error'
    return jsonify({'state': state })

  feed, articles = parse_feed(url, content)

  if feed:
    feed['user_id'] = user_id
    feed['id'] = da.gen_id('feeds')

    da.save_feed(feed)

    for item in articles:
      item['id'] = da.gen_id('articles')
      item['feed_id'] = feed['id']
      da.save_article(item)
    
  return jsonify({ 'state': state, 'feed': feed, 'articles': articles })

def get_feedlist(user_id):
  feedlist = da.get_feedlist(user_id)
  #articles = []
  state = 'ok'
  #if feedlist: 
  #  state = update_feed(feedlist[0])
  #  articles = da.get_articles(feedlist[0]['id'])

  return jsonify({ 'state': state, 'feedlist': feedlist })

def update_feed(feed):
  state = 'ok'
  content = read(feed['url'])
  if not content:
    state = 'network error'
  newfeed, articles = parse_feed(feed['url'], content)
  if newfeed:
    for key in newfeed.keys():
      feed[key] = newfeed[key]

    for item in articles:
      if da.get_article(feed['id'], item['link']): continue
      item['id'] = da.gen_id('articles')
      item['feed_id'] = feed['id']
      da.save_article(item)

  return state

def get_articles(feed_id):
  """
    update article database, return all the articles for feed
  """
  state = update_feed(da.get_feed(feed_id))
  return jsonify({ 'state': state, 'articles': da.get_articles(feed_id) })

