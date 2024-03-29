import httplib2
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lxml import etree
from StringIO import StringIO
from collections import defaultdict
from utils import urlnorm
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
import settings
from models.feed import Feed, Subscription

class Importer:
  def clear_feeds(self):
    pass

  def clear_folders(self):
    pass

class GoogleOAuth:
  def __init__(self, redirect_uri):
    self._oauth_webserver_flow = OAuth2WebServerFlow(
        client_id = settings.GOOGLE_OAUTH2_CLIENT_ID,
        client_secret = settings.GOOGLE_OAUTH2_SECRET,
        scope = settings.GOOGLE_READER_API, # GOOGLE_API
        redirect_uri = redirect_uri,
        user_agent = "reader4you, www.reader4you.com",
        approval_prompt="force",
        )

  def step1_get_authorize_url(self):
    return self._oauth_webserver_flow.step1_get_authorize_url()

  def step2_get_credential(self, code):
    try:
      return self._oauth_webserver_flow.step2_exchange(code)
    except FlowExchangeError:
      return None

class GoogleReaderImporter(Importer):
  def __init__(self, credential):
    self._credential = credential

  def import_feeds(self):
    sub_url = '%s/0/subscription/list' % settings.GOOGLE_READER_API

    http = httplib2.Http()
    http = self._credential.authorize(http)
    content = http.request(sub_url)
    print content
    open("gr_feeds.xml", "w").write(content[1])
    feeds_xml = content and content[1]
    feeds = self._parse(feeds_xml)

    return [self._process_item(item) for item in feeds]

  def _parse(self, feeds_xml):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(StringIO(feeds_xml), parser)
    feeds = tree.xpath('/object/list/object')
    return feeds
  
  def _process_item(self, item):
    feed_title = item.xpath('./string[@name="title"]') and \
                          item.xpath('./string[@name="title"]')[0].text
    feed_address = item.xpath('./string[@name="id"]') and \
                    item.xpath('./string[@name="id"]')[0].text.replace('feed/', '', 1)
    feed_link = item.xpath('./string[@name="htmlUrl"]') and \
                    item.xpath('./string[@name="htmlUrl"]')[0].text
    category = item.xpath('./list[@name="categories"]/object/string[@name="label"]') and \
                    item.xpath('./list[@name="categories"]/object/string[@name="label"]')[0].text
    
    if not feed_address:
        feed_address = feed_link
  
    try:
      feed_link = urlnorm.normalize(feed_link)
      feed_address = urlnorm.normalize(feed_address)
  
      feed = {
          'title': feed_title,
          'url': feed_address,
          'link': feed_link,
          'category': category,
          }
      return feed
  
    except Exception, e:
      print '---->Exception: %s: %s' % (e, item)
  
    return folders
