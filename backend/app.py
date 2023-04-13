from apiflask import APIFlask
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import subprocess
import os
from strip_ansi import strip_ansi


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


@app.get('/projects/<project_id>/settings')
def get_project_settings(project_id):
    command_magecloud = f"magento-cloud project:curl -p {project_id} /settings"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/environments/<project_id>')
def get_environments(project_id):
    command_magecloud = f"magento-cloud environments -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/environments/<project_id>/<environment>/info')
def get_environment_info(project_id, environment):
    command_magecloud = f"magento-cloud environment:info -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/environments/<project_id>/<environment>/url')
def get_environment_url(project_id, environment):
    command_magecloud = f"magento-cloud environment:url -p {project_id} -e {environment} --primary --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/environments/<project_id>/<environment>/relationships')
def get_environment_relationships(project_id, environment):
    command_magecloud = f"magento-cloud environment:relationships -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/files/<project_id>/<environment>')
@app.get('/files/<project_id>/<environment>/<path:filepath>')
def get_files(project_id, environment, filepath='/'):
    command_magecloud = f"magento-cloud read -p {project_id} -e {environment} {filepath}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/variables/<project_id>')
@app.get('/variables/<project_id>/<environment>')
@app.get('/variables/<project_id>/<environment>/<level>')
def get_variables(project_id, environment='master', level='p'):
    command_magecloud = f"magento-cloud variables -p {project_id} -e {environment} -l {level} -c name,value --format plain"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/webui/<project_id>')
@app.get('/webui/<project_id>/<environment>')
def get_webui(project_id, environment='master'):
    command_magecloud = f"magento-cloud web -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/ssh/<project_id>/<environment>')
def get_ssh(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --all --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/versions/<project_id>/<environment>/magento')
def get_versions_magento(project_id, environment):
    # command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} 'composer licenses | head -3 | grep Version'"
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/versions/<project_id>/<environment>/ece-tools')
def get_versions_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/versions/<project_id>/<environment>/nginx')
def get_versions_nginx(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'/usr/sbin/nginx -v\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/versions/<project_id>/<environment>/php')
def get_versions_php(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'php -v | head -1\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/services/<project_id>/<environment>')
def get_services(project_id, environment):
    command_magecloud = f"magento-cloud services -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/users/<project_id>')
def get_users(project_id):
    command_magecloud = f"magento-cloud users -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/disk/<project_id>/<environment>')
@app.get('/disk/<project_id>/<environment>/<int:instance>')
def get_disk(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'df -h\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'df -h\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/mounts/<project_id>/<environment>')
@app.get('/mounts/<project_id>/<environment>/<mountget>')
def get_mounts(project_id, environment, mountget='list'):
    if mountget == 'size':
        command_magecloud = f"magento-cloud mount:{mountget} -p {project_id} -e {environment}"
    else:
        command_magecloud = f"magento-cloud mount:list -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@app.get('/db/<project_id>/<environment>/size')
def get_db_size(project_id, environment):
    command_magecloud = f"magento-cloud db:size -p {project_id} -e {environment} -r database"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/db/<project_id>/<environment>/version')
def get_db_version(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SELECT VERSION();\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/db/<project_id>/<environment>/process')
def get_db_process(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@app.get('/commits/<project_id>/<environment>')
@app.get('/commits/<project_id>/<environment>/<commit>')
def get_commits(project_id, environment, commit='list'):
    if commit == 'list':
        command_magecloud = f"magento-cloud commit:list -p {project_id} -e {environment} --format plain"
    else:
        command_magecloud = f"magento-cloud commit:get -p {project_id} -e {environment} \'{commit}\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
