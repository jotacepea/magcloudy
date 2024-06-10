from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

ssh_bp = APIBlueprint('ssh-blueprint', __name__)

get_db_host_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].host"
get_db_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].port"
get_db_user_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].username"
get_db_pass_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .database[].password"


@ssh_bp.get('/ssh/<project_id>/<environment>/<appid>')
def get_ssh(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --all --pipe"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@ssh_bp.get('/ssh/instance/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/instance/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_instance(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'echo web container $MAGENTO_CLOUD_ENVIRONMENT for $MAGENTO_CLOUD_PROJECT\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'/etc/profile.d/motd.sh | grep server\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/load/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/load/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_load(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'w\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'w\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/fpm/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/fpm/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_fpm(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'ps axuf | grep fpm | grep -v grep\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'ps axuf | grep -A16 \"runsv site-$USER-php\" | grep -vi root | grep -v grep\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/cpu/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/cpu/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_cpu(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'lscpu\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'lscpu\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/free/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/free/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_free(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'free -h\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'free -h\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/crontab/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/crontab/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_crontab(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'crontab -l\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'crontab -l\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/ptmysqlsummary/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/ptmysqlsummary/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_ptmysqlsummary(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'pt-mysql-summary --version\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \'pt-mysql-summary --host $(" + \
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

@ssh_bp.get('/ssh/platformcluster/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/platformcluster/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_platform_cluster(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \"grep 'PLATFORM_CLUSTER=' /etc/profile.d/motd.sh | awk -F'=' '{{print \$2}}'  \" "
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'echo $PLATFORM_CLUSTER\' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/nginxsyntax/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/nginxsyntax/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_nginx_syntax(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \"\$(whereis nginx | awk '{{print \$2}}') -t \""
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \"\$(whereis nginx | awk '{{print \$2}}') -t -c /etc/platform/\$USER/nginx.conf \" "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/nginxservername/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/nginxservername/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_nginx_server_name(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \"cat /etc/nginx.conf|grep -A5 'listen 8080'|grep 'server_name '|awk '{{print \$2}}' \" "
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \"cat /etc/platform/\$USER/nginx.conf|grep -A5 'listen 8080'|grep 'server_name '|awk '{{print \$2}}' \" "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@ssh_bp.get('/ssh/nginxlisten/<project_id>/<environment>/<appid>')
@ssh_bp.get('/ssh/nginxlisten/<project_id>/<environment>/<appid>/<int:instance>')
def get_ssh_nginx_listen(project_id, environment, appid, instance=0):
    if instance == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} \"lsof -P -i -n | grep nginx | grep LISTEN | head\" "
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} -I {instance} \'lsof -P -i -n | grep nginx | grep LISTEN | head\' "
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
