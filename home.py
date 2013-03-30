"""
  
  :copyright: (c) 2013 by Aldrich Huang.
  :license: BSD, see LICENSE for more detials.
"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify
import engine

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
  user_id = request.args.get('user_id')
  return engine.get_feedlist(user_id)

@app.route('/get_articles')
def get_articles():
  feed_id = request.args.get('feed_id')
  print feed_id
  return engine.get_articles(feed_id)

@app.route('/')
def home():
  if not session.get('user_id', None):
    return render_template('login.html')
  return render_template('home.html');

if __name__ == '__main__':
  SERVER_NAME = '127.0.0.1'
  SERVER_PORT = 5050

  app.run(SERVER_NAME, SERVER_PORT, debug=True)

