from apiflask import APIBlueprint
from apiflask.fields import Integer
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


get_redis_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .redis[].port"


@redis_bp.get('/redis/<project_id>/<environment>/bigkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_bigkeys(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --bigkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -h redis.internal --bigkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/memkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_memkeys(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --memkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -h redis.internal --memkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/hotkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_hotkeys(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --hotkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'redis-cli -h redis.internal --hotkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
