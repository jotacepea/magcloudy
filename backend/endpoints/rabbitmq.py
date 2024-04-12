from apiflask import APIBlueprint
from apiflask.fields import Integer
import subprocess
import os
from strip_ansi import strip_ansi

rabbitmq_bp = APIBlueprint('rabbitmq-blueprint', __name__)

get_rabbit_user_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .rabbitmq[].username"
get_rabbit_pass_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .rabbitmq[].password"
get_rabbit_port_cmd = "echo $MAGENTO_CLOUD_RELATIONSHIPS | base64 -d | jq -r .rabbitmq[].port | xargs echo -n"

@rabbitmq_bp.get('/rabbitmq/<project_id>/<environment>/version')
@rabbitmq_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_version_rabbitmq(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u $USER:$(" + \
            f"{get_rabbit_pass_cmd}" + \
            ") -sk http://localhost:1" + "$(" + f"{get_rabbit_port_cmd}" + ")" + "/api/overview |jq .|grep version\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/overview |json_pp |grep version\'"
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
def get_listqueues_rabbitmq(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u $USER:$(" + \
            f"{get_rabbit_pass_cmd}" + \
            ") -sk http://localhost:1" + "$(" + f"{get_rabbit_port_cmd}" + ")" + "/api/queues |jq -r .[].name\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/queues |json_pp|grep name\'"
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
def get_show_rabbitmq(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u $USER:$(" + \
            f"{get_rabbit_pass_cmd}" + \
            ") -sk http://localhost:1" + "$(" + f"{get_rabbit_port_cmd}" + ")" + "/api/overview | jq .\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/overview | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@rabbitmq_bp.get('/rabbitmq/<project_id>/<environment>/healthchecks')
@rabbitmq_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_healthchecks_rabbitmq(project_id, environment, query_data):
    print(query_data['containerized'])
    if query_data['containerized'] == 0:
        #TODO!!
        #for i in range(1,4):
            command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -I 3 \'curl -u $USER:$(" + \
                f"{get_rabbit_pass_cmd}" + \
                ") -sk http://localhost:1" + "$(" + f"{get_rabbit_port_cmd}" + ")" + "/api/healthchecks/node | jq .\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/healthchecks/node | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
