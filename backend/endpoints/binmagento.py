from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

binmagento_bp = APIBlueprint('binmagento-blueprint', __name__)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/version')
def get_version_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/defaulturl')
def get_defaulturl_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento config:show:default-url\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/storeurl')
def get_storeurl_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento config:show:store-url | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/cmspageurl')
def get_cmspageurl_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento config:show:urls --entity-type cms-page | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/maintenance')
def get_maintenance_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'bin/magento maintenance:status\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@binmagento_bp.get('/binmagento/<project_id>/<environment>/consumers')
def get_consumers_binmagento(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'queue:consumers:list\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
