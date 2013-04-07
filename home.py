"""
  
  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify
from flask.helpers import make_response
import engine
import rss_importer
from models.user import User
from models.feed import Feed, Story
import settings
from tools import jsonify

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None

  if request.method == 'POST':
    user = User.get_by_name(request.form['username'])
    if not user and settings.DEBUG == 'debug':
      user = User(request.form['username'], request.form['password'])
      user.save()

    if not user:
      error = 'Invalid username'
    elif user.password != request.form['password']:
      error = 'Invalid password'
    else:
      session['user_id'] = user.user_id
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
  return jsonify(engine.subscribe(session['user_id'], url))

@app.route('/get_feedlist')
def get_feedlist():
  user_id = session['user_id'] 
  return jsonify(engine.get_feedlist_for_user(user_id))

@app.route('/get_stories')
def get_stories():
  feed_id = request.args.get('feed_id')

  offset = int(request.args.get('offset', 0))
  page = int(request.args.get('page', -1));
  limit = int(request.args.get('limit', 6))

  if page >= 0: offset = page * limit

  state = 'ok'
  stories = Story.get_stories_for_feed(feed_id, offset, limit)

  return jsonify({ 
    'state': state, 
    'stories': sorted(stories, key=lambda x: x.publish_date, reverse=True)
    })

@app.route('/reader/google_reader_authorize')
def google_reader_authorize():
  redirect_uri = request.url_root[:-1] + url_for('google_reader_callback')
  
  return redirect(rss_importer.GoogleOAuth(redirect_uri).step1_get_authorize_url())

@app.route('/import/callback')
def google_reader_callback():
  redirect_uri = request.url_root[:-1] + url_for('google_reader_callback')
  
  credential = rss_importer.GoogleOAuth(redirect_uri).step2_get_credential(request.args.get('code'))
  if credential:
    session['credential'] = credential 
    session['import_rss'] = True
  else:
    render_template('import_rss.html', error='hello')

  return render_template('import_rss.html')

@app.route('/import/import_google_reader_rss')
def import_google_reader_rss():
  importer = rss_importer.GoogleReaderImporter(session['credential'])
  return jsonify(engine.subscribe_imported_feeds(session['user_id'], importer.import_feeds()))

@app.route('/import/fetch_history_stories', methods=['POST'])
def fetch_history_stories():
  return jsonify(engine.fetch_history_stories(request.json['feed_ids']))

@app.route('/')
def home():
  if not session.get('user_id', None):
    return render_template('login.html')
  return render_template('home.html');

@app.route('/admin')
def admin():
  if not session.get('user_id'):
    return redirect(url_for('home'))
  return render_template('admin.html')

if __name__ == '__main__':
  SERVER_NAME = '127.0.0.1'
  SERVER_PORT = 8000

  app.run(SERVER_NAME, SERVER_PORT, debug=True)

