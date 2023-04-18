from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

disk_bp = APIBlueprint('disk-blueprint', __name__)


@disk_bp.get('/disk/<project_id>/<environment>')
@disk_bp.get('/disk/<project_id>/<environment>/<int:instance>')
def get_disk(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'df -h\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'df -h\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
