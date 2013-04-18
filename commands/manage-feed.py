import utils.urlnorm as urlnorm
import utils.feedfinder as feedfinder
import urllib2
import urllib
import datetime
import os
from models.feed import Feed

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-l', '--list', dest='list_feeds', action='store_true', default=False, help='list all feeds')
  parser.add_option('-f', '--full', dest='full', action='store_true', default=False, help='show full information')
#  parser.add_option('-u', '--update', dest='
  parser.add_option('-n', dest='n', help='number of stories to fetch', type='int', default=9999)
  parser.add_option('-o', '--output-path', dest='output_path', default='feed_data', help='output path', metavar='FILE')
  parser.add_option('-q', '--quite', dest='quite', action='store_true', default=False, help='turn off log')

  (options, args) = parser.parse_args()

  print options.quite
  if os.path.exists(options.output_path):
    if options.filename == 'db':
      urls = [feed.feed_address for feed in  Feed.get_all_feeds()]
    else: 
      try:
        urls = open(options.filename).readlines()
      except Exception, e:
        print e
        urls = []
    fetch_feeds(urls, options.n, options.output_path, {'quite':options.quite})
  else:
    print 'output path not exists'

