import utils.urlnorm as urlnorm
import utils.feedfinder as feedfinder
import urllib2
import urllib
import datetime
import os

def refresh_feeds(options):
  from models.feed import Feed
  feeds = Feed.get_all()
  for feed in feeds: feed.update(force=True) 

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-l', '--list', dest='list_feeds', action='store_true', default=False, help='list all feeds')
  parser.add_option('-f', '--full', dest='full', action='store_true', default=False, help='show full information')
  parser.add_option('-u', '--update', dest='update', action='store_true', default=False, help='update feeds')
  parser.add_option('-n', '--nthreads', dest='nthreads', type='int', default=1, help='number of threads')


  (options, args) = parser.parse_args()

  if options.update:
    refresh_feeds({
      'nthreads': options.nthreads,
      })
  else:
    pass

