from apiflask import APIFlask, APIBlueprint
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import subprocess
import os
from strip_ansi import strip_ansi

# Import other endpoint definitions (BluePrints)
from endpoints.ecetools import ecetools_bp
from endpoints.commits import commits_bp
from endpoints.activities import activities_bp
from endpoints.db import db_bp
from endpoints.redis import redis_bp
from endpoints.mounts import mounts_bp
from endpoints.disk import disk_bp
from endpoints.users import users_bp
from endpoints.apps import apps_bp
from endpoints.workers import workers_bp
from endpoints.services import services_bp
from endpoints.versions import versions_bp
from endpoints.ssh import ssh_bp
from endpoints.webui import webui_bp
from endpoints.variables import variables_bp
from endpoints.files import files_bp
from endpoints.environments import environments_bp
from endpoints.projects import projects_bp
from endpoints.binmagento import binmagento_bp
from endpoints.rabbitmq import rabbitmq_bp
from endpoints.opensearch import opensearch_bp

# print(os.environ['MAGENTO_CLOUD_CLI_TOKEN'])
default_service_port = os.environ.get("DEFAULT_SERVICE_PORT", "5000")

# app = Flask(__name__)
app = APIFlask(__name__, title='MagCloudy API', version='0.0.1')
CORS(app)

# register BluePrints
app.register_blueprint(ecetools_bp)
app.register_blueprint(commits_bp)
app.register_blueprint(activities_bp)
app.register_blueprint(db_bp)
app.register_blueprint(redis_bp)
app.register_blueprint(mounts_bp)
app.register_blueprint(disk_bp)
app.register_blueprint(users_bp)
app.register_blueprint(apps_bp)
app.register_blueprint(workers_bp)
app.register_blueprint(services_bp)
app.register_blueprint(versions_bp)
app.register_blueprint(ssh_bp)
app.register_blueprint(webui_bp)
app.register_blueprint(variables_bp)
app.register_blueprint(files_bp)
app.register_blueprint(environments_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(binmagento_bp)
app.register_blueprint(rabbitmq_bp)
app.register_blueprint(opensearch_bp)


def bootstrap_magecli():
    command_bootstrap = "magento-cloud ssh-cert:load --no-interaction"
    try:
        result_command_bootstrap = subprocess.check_output(
            [command_bootstrap], shell=True, env=os.environ, universal_newlines=True).split('\n')
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_bootstrap
# bootstrap_magecli()


@app.route('/')
@app.doc(summary='Say hello', description='Default page.')
def index():
    return "Hi from MagCloudy API!!"


pong = [
    {'description': 'healthcheck', 'status': "pong"}
]


@app.route('/ping')
def health():
    return jsonify(pong)


@app.route('/mgcliversion')
@cross_origin(origin='*')
def get_magecli_version():
    command_version = "magento-cloud -V"
    try:
        result_command_version = subprocess.check_output(
            [command_version], shell=True, env=os.environ, universal_newlines=True).split('\n')
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_version


@app.route('/mgcliauth')
@cross_origin(origin='*')
def get_magecli_auth():
    command_auth = "magento-cloud auth:info"
    try:
        result_command_auth = subprocess.check_output(
            [command_auth], shell=True, env=os.environ, universal_newlines=True).split('\n')
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_auth


@app.route('/mgclilist')
@cross_origin(origin='*')
def get_check():
    command_list = "magento-cloud list"
    try:
        result_command_list = subprocess.check_output(
            [command_list], shell=True, env=os.environ, universal_newlines=True).split('\n')
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_list


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=default_service_port)
