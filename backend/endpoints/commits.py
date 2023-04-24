from apiflask import APIBlueprint
import subprocess
import os

commits_bp = APIBlueprint('commits-blueprint', __name__)


@commits_bp.get('/commits/<project_id>/<environment>')
@commits_bp.get('/commits/<project_id>/<environment>/<commit>')
def get_commits(project_id, environment, commit='list'):
    if commit == 'list':
        command_magecloud = f"magento-cloud commit:list -p {project_id} -e {environment} --format plain"
    else:
        command_magecloud = f"magento-cloud commit:get -p {project_id} -e {environment} \'{commit}\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
