from apiflask import APIBlueprint
from apiflask.fields import String
import subprocess
import os
from strip_ansi import strip_ansi

environments_bp = APIBlueprint('environments-blueprint', __name__)


@environments_bp.get('/environments/<project_id>')
@environments_bp.get('/environments/<project_id>/<active>')
def get_environments(project_id, active='active'):
    if active == 'all':
        command_magecloud = f"magento-cloud environments -p {project_id}"
    else:
        command_magecloud = f"magento-cloud environments -I -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@environments_bp.get('/environments/<project_id>/pipe')
def get_environment_pipe(project_id):
    command_magecloud = f"magento-cloud environments -I -p {project_id} --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@environments_bp.get('/environments/<project_id>/<environment>/info')
def get_environment_info(project_id, environment):
    command_magecloud = f"magento-cloud environment:info -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@environments_bp.get('/environments/<project_id>/<environment>/url')
def get_environment_url(project_id, environment):
    command_magecloud = f"magento-cloud environment:url -p {project_id} -e {environment} --primary --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


#TODO: add option to choose APP when app and worker running in the same env.
@environments_bp.get('/environments/<project_id>/<environment>/<appid>/relationships')
def get_environment_relationships(project_id, environment, appid):
    command_magecloud = f"magento-cloud environment:relationships -p {project_id} -e {environment} -A {appid} --no-interaction"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@environments_bp.get('/environments/<project_id>/<environment>/enablesmtpstatus')
def get_environment_enablesmtpstatus(project_id, environment):
    command_magecloud = f"magento-cloud env:info enable_smtp -p {project_id} -e {environment} --no-interaction"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@environments_bp.get('/environments/<project_id>/<environment>/deploymentstatecrons')
def get_environment_deploymentstatecrons(project_id, environment):
    command_magecloud = f"magento-cloud env:info deployment_state.crons -p {project_id} -e {environment} --no-interaction"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
