from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

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
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('home'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('login'))

@app.route('/add_feed', methods=['POST'])
def add_feed():
  print request.form['feed_url']
  return redirect(url_for('home'))

@app.route('/')
def home():
  if not session.get('logged_in', None):
    return render_template('login.html')
  feedList = [ {
      'name': 'test0',
      'url': 'http://www.qq.com'
    },
    {
      'name': 'test1',
      'url': 'http://www.baidu.com'
      }];
  return render_template('home.html', feedList=feedList)

if __name__ == '__main__':
  SERVER_NAME = '127.0.0.1'
  SERVER_PORT = 5050

  app.run(SERVER_NAME, SERVER_PORT, debug=True)

