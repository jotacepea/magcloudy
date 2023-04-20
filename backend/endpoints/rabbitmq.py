from apiflask import APIBlueprint
from apiflask.fields import Integer
import subprocess
import os
from strip_ansi import strip_ansi

rabbitmq_bp = APIBlueprint('rabbitmq-blueprint', __name__)


@rabbitmq_bp.get('/rabbitmq/<project_id>/<environment>/version')
@rabbitmq_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_version_rabbitmq(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'rabbitmqadmin --version\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/nodes |json_pp|grep -A2 -B2 rabbit_common|grep version\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@rabbitmq_bp.get('/rabbitmq/<project_id>/<environment>/listqueues')
@rabbitmq_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_listqueues_rabbitmq(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        get_rabbit_pass_cmd = "vendor/bin/ece-tools env:config:show services | grep -A7 rabbitmq: | grep passw |cut -d\"|\" -f3"
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'rabbitmqadmin -V $USER -u $USER -p $(" + \
            f" {get_rabbit_pass_cmd} " + ") list queues\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/queues |json_pp|grep -n name\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@rabbitmq_bp.get('/rabbitmq/<project_id>/<environment>/show')
@rabbitmq_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_show_rabbitmq(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        get_rabbit_pass_cmd = "vendor/bin/ece-tools env:config:show services | grep -A7 rabbitmq: | grep passw |cut -d\"|\" -f3"
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'rabbitmqadmin -V $USER -u $USER -p $(" + \
            f" {get_rabbit_pass_cmd} " + ") show overview\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'rabbitmqadmin -h\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
