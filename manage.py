from flask.ext.script import Manager
from home import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
