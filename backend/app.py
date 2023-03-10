from apiflask import APIFlask
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import subprocess
import os

# print(os.environ['MAGENTO_CLOUD_CLI_TOKEN'])

# app = Flask(__name__)
app = APIFlask(__name__, title='MagCloudy API', version='0.0.1')
CORS(app)

ip_whitelist = ['192.168.1.2', '192.168.1.3']


def valid_ip():
    client = request.remote_addr
    if client in ip_whitelist:
        return True
    else:
        # Check source IP, right now disabled!!!
        # return False
        return True


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


@app.get('/projects')
def get_projects():
    command_magecloud = "magento-cloud project:list"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/projects/<project_id>/info')
def get_project_info(project_id):
    command_magecloud = f"magento-cloud project:info -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
