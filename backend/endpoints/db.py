from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

db_bp = APIBlueprint('db-blueprint', __name__)


@db_bp.get('/db/<project_id>/<environment>/size')
def get_db_size(project_id, environment):
    command_magecloud = f"magento-cloud db:size -p {project_id} -e {environment} -r database"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/version')
def get_db_version(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SELECT VERSION();\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/process')
def get_db_process(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)