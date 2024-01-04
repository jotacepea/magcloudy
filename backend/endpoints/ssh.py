from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

ssh_bp = APIBlueprint('ssh-blueprint', __name__)

get_db_host_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].host"
get_db_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].port"
get_db_user_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].username"
get_db_pass_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].password"


@ssh_bp.get('/ssh/<project_id>/<environment>')
def get_ssh(project_id, environment):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} --all --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


@ssh_bp.get('/ssh/instance/<project_id>/<environment>/<int:instance>')
def get_ssh_instance(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'echo web container $MAGENTO_CLOUD_ENVIRONMENT for $MAGENTO_CLOUD_PROJECT\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'/etc/profile.d/motd.sh | grep server\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ssh_bp.get('/ssh/load/<project_id>/<environment>/<int:instance>')
def get_ssh_load(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'w\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'w\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ssh_bp.get('/ssh/fpm/<project_id>/<environment>/<int:instance>')
def get_ssh_fpm(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'ps axuf | grep fpm | grep -v grep\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'ps axuf | grep fpm | grep pool | grep -v grep\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ssh_bp.get('/ssh/cpu/<project_id>/<environment>/<int:instance>')
def get_ssh_cpu(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'lscpu\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'lscpu\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/free/<project_id>/<environment>/<int:instance>')
def get_ssh_free(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'free -h\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'free -h\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/crontab/<project_id>/<environment>/<int:instance>')
def get_ssh_crontab(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'crontab -l\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'crontab -l\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@ssh_bp.get('/ssh/ptmysqlsummary/<project_id>/<environment>/<int:instance>')
def get_ssh_ptmysqlsummary(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'pt-mysql-summary --version\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'pt-mysql-summary --host $(" + \
            f"{get_db_host_cmd}" + \
            ") --port $(" + \
            f"{get_db_port_cmd}" + \
            ") --user $(" + \
            f"{get_db_user_cmd}" + \
            ") --password $(" + \
            f"{get_db_pass_cmd}" + \
            ")\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/platformcluster/<project_id>/<environment>/<int:instance>')
def get_ssh_platform_cluster(project_id, environment, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \"grep 'PLATFORM_CLUSTER=' /etc/profile.d/motd.sh | awk -F'=' '{{print \$2}}'  \""
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I {instance} \'echo $PLATFORM_CLUSTER\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
