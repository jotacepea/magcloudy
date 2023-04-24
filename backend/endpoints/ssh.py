from apiflask import APIBlueprint
import subprocess
import os

ssh_bp = APIBlueprint('ssh-blueprint', __name__)


@ssh_bp.get('/ssh/<project_id>/<environment>')
def get_ssh(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --all --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
