from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

users_bp = APIBlueprint('users-blueprint', __name__)


@users_bp.get('/users/<project_id>')
def get_users(project_id):
    command_magecloud = f"magento-cloud users -p {project_id}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
