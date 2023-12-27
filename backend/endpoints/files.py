from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

files_bp = APIBlueprint('files-blueprint', __name__)


@files_bp.get('/files/<project_id>/<environment>')
@files_bp.get('/files/<project_id>/<environment>/<path:filepath>')
def get_files(project_id, environment, filepath='/'):
    command_magecloud = f"magento-cloud read -p {project_id} -e {environment} {filepath}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@files_bp.get('/files/live/<project_id>/<environment>/<path:filepath>')
def get_files_live(project_id, environment, filepath):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --no-interaction \'cat ./{filepath}\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
