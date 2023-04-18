from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

projects_bp = APIBlueprint('projects-blueprint', __name__)


@projects_bp.get('/projects')
def get_projects():
    command_magecloud = "magento-cloud project:list"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@projects_bp.get('/projects/<project_id>/info')
def get_project_info(project_id):
    command_magecloud = f"magento-cloud project:info -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@projects_bp.get('/projects/<project_id>/settings')
def get_project_settings(project_id):
    command_magecloud = f"magento-cloud project:curl -p {project_id} /settings"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
