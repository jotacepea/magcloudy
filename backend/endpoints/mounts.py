from apiflask import APIBlueprint
import subprocess
import os

mounts_bp = APIBlueprint('mounts-blueprint', __name__)


@mounts_bp.get('/mounts/<project_id>/<environment>')
@mounts_bp.get('/mounts/<project_id>/<environment>/<mountget>')
def get_mounts(project_id, environment, mountget='list'):
    if mountget == 'size':
        command_magecloud = f"magento-cloud mount:{mountget} -p {project_id} -e {environment}"
    else:
        command_magecloud = f"magento-cloud mount:list -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
