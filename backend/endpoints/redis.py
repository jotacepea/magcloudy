from apiflask import APIBlueprint
from apiflask.fields import Integer
import subprocess
import os
from strip_ansi import strip_ansi

redis_bp = APIBlueprint('redis-blueprint', __name__)


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/ping')
def get_redis_ping(project_id, environment, appid):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis ping"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/info')
def get_redis_info(project_id, environment, appid):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis info"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/sinfo')
def get_redis_server_info(project_id, environment, appid):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis \'INFO SERVER;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@redis_bp.get('/redis/<project_id>/<environment>/<appid>/lazyfreelazy')
def get_redis_server_lazyfreelazy(project_id, environment, appid):
    command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis \'config get lazy\*;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


get_redis_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .redis[].port"


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/bigkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_bigkeys(project_id, environment, appid, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --bigkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -h redis.internal --bigkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/memkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_memkeys(project_id, environment, appid, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --memkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -h redis.internal --memkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@redis_bp.get('/redis/<project_id>/<environment>/<appid>/hotkeys')
@redis_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_redis_hotkeys(project_id, environment, appid, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
            f"{get_redis_port_cmd}" + ") --hotkeys;\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -h redis.internal --hotkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
