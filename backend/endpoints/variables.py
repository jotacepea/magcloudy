from apiflask import APIBlueprint
import subprocess
import os

variables_bp = APIBlueprint('variables-blueprint', __name__)


@variables_bp.get('/variables/<project_id>')
@variables_bp.get('/variables/<project_id>/<environment>')
@variables_bp.get('/variables/<project_id>/<environment>/<level>')
def get_variables(project_id, environment='master', level='p'):
    if level == 'e':
        command_magecloud = f"magento-cloud project:curl -p {project_id} /environments/{environment}/variables | jq -r ."
    elif level == 'p':
        command_magecloud = f"magento-cloud project:curl -p {project_id} /variables | jq -r ."
    else:
        return "Invalid var level"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
