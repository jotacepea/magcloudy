from apiflask import APIBlueprint
import subprocess
import os

users_bp = APIBlueprint('users-blueprint', __name__)


@users_bp.get('/users/<project_id>')
def get_users(project_id):
    command_magecloud = f"magento-cloud project:curl -p {project_id} /access"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@users_bp.get('/users/<project_id>/owner')
def get_users_owner(project_id):
    command_magecloud = f"magento-cloud subscription:info -p {project_id} -q owner_info"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud