from apiflask import APIBlueprint
import subprocess
import os

workers_bp = APIBlueprint('workers-blueprint', __name__)


@workers_bp.get('/workers/<project_id>/<environment>')
def get_workers(project_id, environment):
    command_magecloud = f"magento-cloud workers -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
