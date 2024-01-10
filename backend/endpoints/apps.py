from apiflask import APIBlueprint
from apiflask.fields import Integer, String
import subprocess
import os

apps_bp = APIBlueprint('apps-blueprint', __name__)


@apps_bp.get('/apps/<project_id>/<environment>')
@apps_bp.input(
    {'format': String(load_default='table'),
     'columns': String(load_default='*'),
     'header': Integer(load_default=1)},
    location='query'
)
def get_apps(project_id, environment, query_data):
    outputype = query_data['format']
    colulist = query_data['columns']
    if query_data['header'] == 0:
        command_magecloud = f"magento-cloud apps -p {project_id} -e {environment} --format {outputype} -c '{colulist}' --no-header"
    else:
        command_magecloud = f"magento-cloud apps -p {project_id} -e {environment} --format {outputype} -c '{colulist}' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
