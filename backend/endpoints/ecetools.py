from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

ecetools_bp = APIBlueprint('ece-tools-blueprint', __name__)


@ecetools_bp.get('/ece-tools/<project_id>/<environment>/version')
def get_version_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ecetools_bp.get('/ece-tools/<project_id>/<environment>/validate')
def get_validate_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools cloud:config:validate\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ecetools_bp.get('/ece-tools/<project_id>/<environment>/config')
def get_config_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools env:config:show\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ecetools_bp.get('/ece-tools/<project_id>/<environment>/error')
def get_error_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools error:show\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ecetools_bp.get('/ece-tools/<project_id>/<environment>/wizards')
def get_wizards_ecetools(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'vendor/bin/ece-tools list wizard|egrep Verifies|cut -dV -f1|xargs -n1 vendor/bin/ece-tools || exit 0\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
