import utils.urlnorm as urlnorm
import utils.feedfinder as feedfinder
import urllib2
import urllib
import datetime
import os

def fetch(rss_url, n, out_path, options):
  try:
    url = ('https://www.google.com/reader/public/atom/feed/%s?n=%d' % (rss_url, n))
    if not options['quite']: 
      print '[fetching]:' 
      print '     %s' % url
    path = os.path.join(out_path, ('%s+%s+%d.txt' % (urllib.quote(rss_url.replace('/','-')), datetime.datetime.utcnow(), n)))
    open(path, 'w').write(urllib2.urlopen(url, timeout=20).read())
    if not options['quite']: print 'fetch complete'
  except Exception, e:
    print e

def fetch_feeds(urls, n, output_path, options):
  if not options['quite']: print 'fetch feeds'
  for url in urls:
    url = urlnorm.normalize(url)
    if True or feedfinder.isFeed(url):
      fetch(url, n, output_path, options)
    else:
      print '%s is not a feed url' % url

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-f', '--file', dest='filename', default='db', help='the file contains feed urls, or [db] to get feed urls from database', metavar='FILE')
  parser.add_option('-n', dest='n', help='number of stories to fetch', type='int', default=99999)
  parser.add_option('-o', '--output-path', dest='output_path', default='feed_data', help='output path', metavar='FILE')
  parser.add_option('-q', '--quite', dest='quite', action='store_true', default=False, help='turn off log')

  (options, args) = parser.parse_args()

  if os.path.exists(options.output_path):
    if options.filename == 'db':
      from models.feed import Feed
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

