from flask import Flask
from flask_script import Manager
#from APPs import create_app
from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from settings import Config
from APPs import policy
#app=create_app()
from flask_bootstrap import Bootstrap

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#templates_dir = os.path.join(BASE_DIR, 'templates')
#static_dir = os.path.join(BASE_DIR, 'static')
templates_dir='templates'
static_dir='static'
app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)
bootstrap=Bootstrap(app)
app.config.from_object(Config)
#engine=create_engine(Config.SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy(app)
db.init_app(app)
app.register_blueprint(blueprint=policy,url_prefix='/policy') # 将app交由blue管理
app.app_context().push()
db.init_app(app)
manager=Manager(app=app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
