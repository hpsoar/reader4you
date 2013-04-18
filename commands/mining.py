import feedparser
import os
import datetime
from BeautifulSoup import BeautifulSoup as Soup
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lxml import etree
from StringIO import StringIO

class GRXMLFeed:
  def __init__(self, path):
    starttime = datetime.datetime.now()
    content = open(path).read()
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(StringIO(content), parser)
    self.root = tree.getroot()
    self.ns = {'n': self.root.nsmap[None]}
    endtime = datetime.datetime.now() 
    print '-' * 80
    print('(%s-%s) : %s' % (starttime, endtime, endtime-starttime))

  def make_tag(self, tag):
    return '{%s}%s' % (ns, tag)

  def extract_story(self, e):
    story = {}
    story['title'] = e.xpath('.//n:title', namespaces=self.ns)[0].text
    story['content'] = e.xpath('.//n:content', namespaces=self.ns)[0].text
    link = e.xpath('.//n:link', namespaces=self.ns)
    story['link'] = link[0].get('href', '')
    return story


  def extract_stories(self):
    return [self.extract_story(e) for e in self.root.xpath('.//n:entry', namespaces=self.ns)]

def process(path):
  if not os.path.exists(path):
    print '%s not exists' % path
  
  if os.path.isfile(path):
    xml_feed = GRXMLFeed(path)
    return xml_feed.extract_stories()

  if not os.path.isdir(path):
    print 'not a path'

  stories = []
  for dir_path, subpaths, filenames in os.walk(path):
    for filename in filenames:
      xml_feed = GRXMLFeed(os.path.join(dir_path, filename))
      stories += xml_feed.extract_stories()
  return stories

if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    print 'Usage: python mining.py -d path'

  stories = process(sys.argv[1])
  # extract xml tags in content
