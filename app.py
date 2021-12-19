from flask import Flask, render_template
from flask_restful import Api
from db import db
from resources.game import GameByCategory, GameByPlatform, GameList
from resources.checkhealth import CheckHealth
from resources.recreate import ReCreateSchema
import os
import logging
import logging.config
import watchtower
import hvac
import pymysql
import urllib.request
import boto3

AWS_REGION_NAME = 'eu-west-1'

boto3_logs_client = boto3.client("logs", region_name=AWS_REGION_NAME)

log_level = {
  'CRITICAL' : 50,
  'ERROR'	   : 40,
  'WARN'  	 : 30,
  'INFO'	   : 20,
  'DEBUG'	   : 10
}
logger = logging.getLogger("werkzeug")

app = Flask("CloudSchool-App")

app.config.from_pyfile("app.conf", silent=False)

RAPID_API_KEY = app.config.get("RAPID_API_KEY")
END_POINT = app.config.get("END_POINT")
MYSQL_ENDPOINT = (app.config.get("MYSQL_ENDPOINT")).split(":")[0]
LOG_LEVEL = app.config.get("LOG_LEVEL")
SCHEMA_NAME = app.config.get("SCHEMA_NAME")
VAULT_ENDPOINT = app.config.get("VAULT_ENDPOINT")
VAULT_TOKEN = app.config.get("VAULT_TOKEN")
VAULT_PATH_TO_CREDS = app.config.get("VAULT_PATH_TO_CREDS")
APPLICATION_VERSION = app.config.get("APPLICATION_VERSION")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' #'sqlite:///data.db'
#app.config['SQLALCHEMY_BINDS'] = {SCHEMA_NAME: SQL_CONNECTION_STRING + SCHEMA_NAME}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

VAULT_CLIENT = hvac.Client(url=VAULT_ENDPOINT, token=VAULT_TOKEN)
api = Api(app)

api.add_resource(GameByCategory, '/category/<string:name>')
api.add_resource(GameByPlatform, '/platform/<string:name>')
api.add_resource(GameList, '/games')
api.add_resource(CheckHealth, '/checkhealth')
api.add_resource(ReCreateSchema, '/recreate')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def not_found500(error):
    return render_template('error.html'), 500

@app.before_first_request
def create_tables():
    logger.info("Preparing database {}...".format(db))
    db.session.execute(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
    db.create_all()

def _get_db_connector():
    logger.info('Get credentials for database from Vault')
    resp = VAULT_CLIENT.read(VAULT_PATH_TO_CREDS)
    host = MYSQL_ENDPOINT
    user= resp['data']['username']
    password = resp['data']['password']
    connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=SCHEMA_NAME)

    return connection

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"creator" : _get_db_connector}
logging.basicConfig(
    level=log_level[LOG_LEVEL],
    format='%(asctime)s - %(levelname)8s - %(name)9s - %(funcName)15s - %(message)s'
)
instanceid = "local"
try:
    instanceid = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
except:
    pass
handler = watchtower.CloudWatchLogHandler(stream_name=f"AppVersion-{APPLICATION_VERSION}-werkzeug-{instanceid}",                                          log_group_name=app.name, boto3_client=boto3_logs_client)
app.logger.addHandler(handler)
logging.getLogger("werkzeug").addHandler(handler)
db.init_app(app)
logger.info('Starting Flask server on {} listening on port {}'.format('0.0.0.0', '5000'))

if __name__ == '__main__':
    app.run() #host= "0.0.0.0", port = 5000, debug=True)