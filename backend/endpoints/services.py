from apiflask import APIBlueprint
import subprocess
import os

services_bp = APIBlueprint('services-blueprint', __name__)


@services_bp.get('/services/<project_id>/<environment>')
def get_services(project_id, environment):
    command_magecloud = f"magento-cloud services -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
