from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

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


@ssh_bp.get('/ssh/instance/<project_id>/<environment>/<int:instance>')
def get_ssh_instance(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'echo web container $MAGENTO_CLOUD_ENVIRONMENT for $MAGENTO_CLOUD_PROJECT\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'/etc/profile.d/motd.sh | grep server\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
