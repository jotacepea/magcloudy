from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

binmagento_bp = APIBlueprint('binmagento-blueprint', __name__)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/version')
def get_version_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento -V\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/defaulturl')
def get_defaulturl_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento config:show:default-url\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/storeurl')
def get_storeurl_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento config:show:store-url | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/cmspageurl')
def get_cmspageurl_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento config:show:urls --entity-type cms-page | json_pp\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/adminurl')
@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/adminurl')
def get_adminurl_binmagento(project_id, environment, appid='mymagento'):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento info:adminuri\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/maintenance')
def get_maintenance_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento maintenance:status\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/consumers')
def get_consumers_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento queue:consumers:list\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/indexer')
def get_indexer_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento indexer:status\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/searchengine')
def get_searchengine_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento config:show catalog/search/engine\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/cache')
def get_cache_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento cache:status\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/stores')
def get_stores_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento store:list -n\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@binmagento_bp.get('/binmagento/<project_id>/<environment>/<appid>/websites')
def get_websites_binmagento(project_id, environment, appid):
    command_magecloud = f"magento-cloud ssh -p {project_id} -e {environment} -A {appid} --no-interaction \'bin/magento store:website:list -n\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)
