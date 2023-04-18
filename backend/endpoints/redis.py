from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

redis_bp = APIBlueprint('redis-blueprint', __name__)


@redis_bp.get('/redis/<project_id>/<environment>/ping')
def get_redis_ping(project_id, environment):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -r redis ping"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/info')
def get_redis_info(project_id, environment):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -r redis info"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/sinfo')
def get_redis_server_info(project_id, environment):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -r redis \'INFO SERVER;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
