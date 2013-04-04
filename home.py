"""
  
  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify
import engine
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
import settings
from flask.helpers import make_response
import httplib2
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lxml import etree
from StringIO import StringIO
from collections import defaultdict
from utils import urlnorm

USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['user_id'] = 'admin'
      flash('You were logged in')
      return redirect(url_for('home'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  flash('You were logged out')
  return redirect(url_for('login'))

@app.route('/add_feed')
def add_feed():
  url = request.args.get('feed_url')
  return engine.add_feed(session['user_id'], url)

@app.route('/get_feedlist')
def get_feedlist():
  user_id = session['user_id'] 
  return engine.get_feedlist(user_id)

@app.route('/get_articles')
def get_articles():
  feed_id = request.args.get('feed_id')
  return engine.get_articles(feed_id)

@app.route('/reader/authorize')
def reader_authorize():
  STEP2_URI = request.url_root[:-1] + url_for('reader_callback')

  FLOW = OAuth2WebServerFlow(
      client_id = settings.GOOGLE_OAUTH2_CLIENT_ID,
      client_secret = settings.GOOGLE_OAUTH2_SECRET,
      scope = settings.GOOGLE_READER_API,
      redirect_uri = STEP2_URI,
      user_agent = "reader4you, www.reader4you.com",
      approval_prompt="force",
      )
  print STEP2_URI
  authorize_url = FLOW.step1_get_authorize_url()
  print authorize_url
  return redirect(authorize_url)

@app.route('/import/callback')
def reader_callback():
  STEP2_URI = request.url_root[:-1] + url_for('reader_callback')

  FLOW = OAuth2WebServerFlow(
      client_id = settings.GOOGLE_OAUTH2_CLIENT_ID,
      client_secret = settings.GOOGLE_OAUTH2_SECRET,
      scope = settings.GOOGLE_READER_API,
      redirect_uri = STEP2_URI,
      user_agent = "reader4you, www.reader4you.com",
      approval_prompt="force",
      )
  
  try:
      credential = FLOW.step2_exchange(request.args.get('code'))
      session['import_rss'] = True
      session['credential'] = credential
  except FlowExchangeError:
    return render_template('import_rss.html', error='hello')

  return render_template('import_rss.html')

def parse(feeds_xml):
  parser = etree.XMLParser(recover=True)
  tree = etree.parse(StringIO(feeds_xml), parser)
  feeds = tree.xpath('/object/list/object')
  return feeds

def process_item(item, folders):
  feed_title = item.xpath('./string[@name="title"]') and \
                        item.xpath('./string[@name="title"]')[0].text
  feed_address = item.xpath('./string[@name="id"]') and \
                  item.xpath('./string[@name="id"]')[0].text.replace('feed/', '')
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
    print feed
    if not category: category = "Root"
    folders[category].append(feed)

  except Exception, e:
    print '---->Exception: %s: %s' % (e, item)

  return folders


@app.route('/import/import_google_reader_rss')
def import_google_reader_rss():
  sub_url = '%s/0/subscription/list' % settings.GOOGLE_READER_API
  http = httplib2.Http()
  http = session['credential'].authorize(http)
  content = http.request(sub_url)
  feeds_xml = content and content[1]
  feeds = parse(feeds_xml)

  folders = defaultdict(list)
  for item in feeds:
      folders = process_item(item, folders)
  return jsonify({'state': 'ok' })

@app.route('/')
def home():
  if not session.get('user_id', None):
    return render_template('login.html')
  return render_template('home.html');

if __name__ == '__main__':
  SERVER_NAME = '127.0.0.1'
  SERVER_PORT = 8000

  app.run(SERVER_NAME, SERVER_PORT, debug=True)

