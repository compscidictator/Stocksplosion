import os
import sys
import subprocess
from flask_script import Manager, Shell, Server

from stocksplosion.app import create_app
from stocksplosion.settings import Config

app = create_app(Config)

manager = Manager(app)

def _make_context():
  return {'app': app, 'db': db, 'User': User}

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
  manager.run()
