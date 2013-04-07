"""
  Feed Engine
  ~~~~~~~~~~~~

  a module manages feeds & articles

  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
import urllib2
import utils.feedfinder as feedfinder
import utils.urlnorm as urlnorm
import time
import datetime
from operator import itemgetter
from models.feed import Feed, Subscription, Story

def subscribe(user_id, url):
  """
  subscribe a feed with address: url

  return: @state 'ok'/'network error'/'duplication'
          @feed feed information
          @articles latested articles
  """
  state = 'ok'
  url = urlnorm.normalize(url)
  if not feedfinder.isFeed(url):
    return {'state': 'invalid feed url'}

  feed, feed_exist = Feed.get_or_create(url)
  
  sub, sub_exist = Subscription.get_or_create(user_id, feed.feed_id)

  print feed
  print sub

  if sub_exist:
    state = 'duplication'
    return {'state': state}

  return { 'state': state, 'feed': feed, 'stories': Story.get_stories_for_feed(feed.feed_id) }

def subscribe_imported_feeds(user_id, items):
  """
  [item${i}: {
    'title': ${title},
    'url': ${url}
    'link': ${link}
    'category': []
  }]
  return: [newly subscribed feeds]
  """
  state = 'ok'
  feedlist = []
  for item in items:
    feed, feed_exist = Feed.get_or_create(item['url'], item['title'], item['link'])
    sub, sub_exist = Subscription.get_or_create(user_id, feed.feed_id)
    if not sub_exist: feedlist.append(feed)
  return { 'state': state, 'feedlist': feedlist }

def get_feedlist_for_user(user_id):
  subs = Subscription.get_by_user(user_id)

  feedlist = [Feed.get_by_id(sub.feed_id) for sub in subs]
  state = 'ok'

  return { 'state': state, 'feedlist': feedlist }

def get_stories_for_feed(feed_id):
  """
    update article database, return all the articles for feed
  """
  state = 'ok'
  stories = Story.get_stories_for_feed(feed_id)
  return { 'state': state, 'stories': sorted(stories, key = lambda x: x.publish_date, reverse=True) }

def fetch_history_stories(feed_ids):
  from  models.fetch_feed_history import HistoryStoryFetcher
  fetcher = HistoryStoryFetcher()
  states = fetcher.add_feeds(feed_ids)
  # start a thread to do the fetch
  fetcher.start()
  #fetcher.join()
  return { 'state':'ok', 'feed_states': states}
