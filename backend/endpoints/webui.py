from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

webui_bp = APIBlueprint('webui-blueprint', __name__)


@webui_bp.get('/webui/<project_id>')
@webui_bp.get('/webui/<project_id>/<environment>')
def get_webui(project_id, environment='master'):
    command_magecloud = f"magento-cloud web -p {project_id} -e {environment}"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
