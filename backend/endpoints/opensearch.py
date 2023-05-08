from apiflask import APIBlueprint
from apiflask.fields import Integer
import subprocess
import os
from strip_ansi import strip_ansi

opensearch_bp = APIBlueprint('opensearch-blueprint', __name__)


@opensearch_bp.get('/opensearch/<project_id>/<environment>/version')
@opensearch_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_version_opensearch(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://localhost:9200/ |jq\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://opensearch.internal:9200/ |json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@opensearch_bp.get('/opensearch/<project_id>/<environment>/health')
@opensearch_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_health_opensearch(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://localhost:9200/_cluster/health |jq\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://opensearch.internal:9200/_cluster/health |json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@opensearch_bp.get('/opensearch/<project_id>/<environment>/indices')
@opensearch_bp.input(
    {'containerized': Integer(load_default=0)},
    location='query'
)
def get_indices_opensearch(project_id, environment, query):
    print(query['containerized'])
    if query['containerized'] == 0:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://localhost:9200/_cat/indices?v\'"
    else:
        command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} \'curl -sk http://opensearch.internal:9200/_cat/indices?v\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
