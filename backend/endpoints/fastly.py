from apiflask import APIBlueprint
from apiflask.fields import String
import subprocess
import os
from strip_ansi import strip_ansi

fastly_bp = APIBlueprint('fastly-blueprint', __name__)


@fastly_bp.get('/fastly/<project_id>/<environment>')
def get_fastly(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --no-interaction \'bin/magento fastly:conf:get -e -s -n --no-ansi\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@fastly_bp.get('/fastly/<project_id>/<environment>/credentials')
def get_fastly_credentials(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --no-interaction \'grep -A2 ${{USER}} /mnt/shared/fastly_tokens.txt\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/service')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_service(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly service describe --non-interactive --quiet --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/backend')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_backend(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly backend list --version active --non-interactive --quiet --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/domain')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_domain(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly domain list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/healthcheck')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_healthcheck(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly healthcheck list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/products')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_products(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly products -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/ratelimit')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_ratelimit(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly rate-limit list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/stats')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_stats(project_id, fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly stats historical -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/tlsconfig')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_tlsconfig(project_id,fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly tls-config list -iq --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/vclcondition')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_vclcondition(project_id,fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly vcl condition list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/vclcustom')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_vclcustom(project_id,fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly vcl custom list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/vclsnippet')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_vclsnippet(project_id,fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly vcl snippet list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@fastly_bp.get('/fastly/<project_id>/<fastly_service_id>/acl')
@fastly_bp.input(
    {'fast_token': String(load_default='tata-123-error-tata-123')},
    location='query'
)    
def get_fastly_acl(project_id,fastly_service_id, query_data):
    print(query_data['fast_token'])
    fast_token = query_data['fast_token']
    command_magecloud = f"fastly acl list --version active -iq --service-id {fastly_service_id} --token {fast_token}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
