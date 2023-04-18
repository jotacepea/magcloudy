from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

versions_bp = APIBlueprint('versions-blueprint', __name__)


@versions_bp.get('/versions/<project_id>/<environment>/magento')
def get_versions_magento(project_id, environment):
    # command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} 'composer licenses | head -3 | grep Version'"
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@versions_bp.get('/versions/<project_id>/<environment>/nginx')
def get_versions_nginx(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'/usr/sbin/nginx -v\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@versions_bp.get('/versions/<project_id>/<environment>/php')
def get_versions_php(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'php -v | head -1\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
