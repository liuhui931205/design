from flask import Flask, jsonify, request
from flask_migrate import Migrate,MigrateCommand
from util import qiniu_auth,utils
from app import app_create,db
from flask_script import Manager
import os

print(os.getenv('FLASK_ENV'))
app = app_create(os.getenv('FLASK_ENV') or 'development')
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
    # manager.run()
