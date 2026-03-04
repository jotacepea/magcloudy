from apiflask import APIBlueprint
from apiflask.fields import Integer
import subprocess
import os
from strip_ansi import strip_ansi

inmemorycache_bp = APIBlueprint('inmemorycache-blueprint', __name__)

# Command helpers

# Get Redis port
get_redis_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .redis[].port"
# Get Valkey port
get_valkey_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .valkey[].port"

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/ping')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_ping(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis PING;"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") ping;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal ping;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/info')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_info(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis INFO;"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") info;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal info;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/sinfo')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_sinfo(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis INFO SERVER;"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") info server;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal info server;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/lazyfreelazy')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_lazyfreelazy(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud redis -p {project_id} -e {environment} -A {appid} -r redis CONFIG GET lazy\*;"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") config get lazy\*;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal config get lazy\*;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/bigkeys')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_bigkeys(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
                f"{get_redis_port_cmd}" + ") -i 0.01 --bigkeys;\'"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") -i 0.01 --bigkeys;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal -i 0.01 --bigkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/memkeys')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_memkeys(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
                f"{get_redis_port_cmd}" + ") -i 0.01 --memkeys;\'"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") -i 0.01 --memkeys;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal -i 0.01 --memkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@inmemorycache_bp.get('/inmemorycache/<cache_service>/<project_id>/<environment>/<appid>/hotkeys')
@inmemorycache_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_inmemorycache_hotkeys(cache_service, project_id, environment, appid, query_data):
    print(query_data['containerized'])
    match cache_service:
        case "redis":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'redis-cli -p $(" + \
                f"{get_redis_port_cmd}" + ") -i 0.01 --hotkeys;\'"
        case "valkey":
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'valkey-cli -p $(" + \
                f"{get_valkey_port_cmd}" + ") -i 0.01 --hotkeys;\'"
        case _:
            return "Error: Invalid cache service API Endpoint"

    if query_data['containerized'] == 0:
        command_magecloud
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'{cache_service}-cli -h {cache_service}.internal -i 0.01 --hotkeys;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

