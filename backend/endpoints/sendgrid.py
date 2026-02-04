from apiflask import APIBlueprint
import subprocess
import os

sendgrid_bp = APIBlueprint('sendgrid-blueprint', __name__)

magento_sendgrid_psh_api_host="magento.sendgrid.pltfrm.sh"

@sendgrid_bp.get('/sendgrid/<project_id>/<environment>')
def get_sendgrid(project_id, environment):
    command_magecloud = f"curl -A \"{project_id}-{environment}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/search/{project_id} | grep -v DELETED"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/info')
def get_sendgrid_info(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/info/{environment_username}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/domains')
def get_sendgrid_domains(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/domain/{environment_username}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/blocklist')
def get_sendgrid_blocklist(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/blocklist/{environment_username}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/stats')
def get_sendgrid_stats(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/stats/{environment_username}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/credit')
def get_sendgrid_credit(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/credit/report/{environment_username} \
        -XPOST -d '{{\"limit\": 90}}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/bounce')
def get_sendgrid_bounce(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/messages/bounce/{environment_username} \
        -XPOST -d '{{\"limit\": 90}}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/dropped')
def get_sendgrid_dropped(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/messages/dropped/{environment_username} \
        -XPOST -d '{{\"limit\": 90}}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/msgget')
def get_sendgrid_messages_get(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/messages/get/{environment_username} \
        -XPOST -d '{{\"limit\": 90}}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@sendgrid_bp.get('/sendgrid/<project_id>/<environment_username>/msghist')
def get_sendgrid_messages_history(project_id, environment_username):
    command_magecloud = f"curl -A \"{project_id}-{environment_username}\" -H \"Authorization: Bearer $(magento-cloud a:t 2>/dev/null)\" -s \
        https://{magento_sendgrid_psh_api_host}/api/v1/sendgrid/messages/history/{environment_username} \
        -XPOST -d '{{\"limit\": 90}}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
