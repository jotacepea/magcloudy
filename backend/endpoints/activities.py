from apiflask import APIBlueprint
import subprocess
import os

activities_bp = APIBlueprint('activities-blueprint', __name__)


@activities_bp.get('/activities/<project_id>/<environment>')
@activities_bp.get('/activities/<project_id>/<environment>/<activity>')
def get_activities(project_id, environment, activity='list'):
    if activity == 'list':
        command_magecloud = f"magento-cloud activity:list -p {project_id} -e {environment} -x cron --limit 15"
    else:
        if activity == 'last':
            command_magecloud = f"magento-cloud activity:get -p {project_id} -e {environment} -x cron"
        else:
            command_magecloud = f"magento-cloud activity:get -p {project_id} -e {environment} \'{activity}\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@activities_bp.get('/activities/log/<project_id>/<environment>/<activity>')
def get_activities_log(project_id, environment, activity='last'):
    if activity == 'last':
        command_magecloud = f"magento-cloud activity:log -p {project_id} -e {environment} -x cron"
    else:
        command_magecloud = f"magento-cloud activity:log -p {project_id} -e {environment} \'{activity}\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud
