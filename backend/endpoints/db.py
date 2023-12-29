from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

db_bp = APIBlueprint('db-blueprint', __name__)


@db_bp.get('/db/<project_id>/<environment>/size')
def get_db_size(project_id, environment):
    command_magecloud = f"magento-cloud db:size -p {project_id} -e {environment} -r database"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/version')
def get_db_version(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SELECT VERSION();\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/status')
def get_db_status(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'status;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/tablesize')
def get_db_tablesize(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SELECT table_schema as `Database`, table_name AS `Table`, ROUND(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` FROM information_schema.TABLES ORDER BY (data_length + index_length) DESC LIMIT 15;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/myisam')
def get_db_myisam(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \"SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE engine = 'MyISAM' AND TABLE_SCHEMA <> 'mysql';\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/primarykey')
def get_db_primarykey(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \"SELECT table_schema, table_name, engine, 'NoPrimKey!!!' FROM information_schema.tables WHERE (table_schema, table_name) NOT IN (SELECT table_schema, table_name FROM information_schema.table_constraints  WHERE constraint_type = 'PRIMARY KEY') AND table_schema NOT IN ('information_schema', 'pg_catalog');\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/wsrep')
def get_db_wsrep(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'SHOW STATUS WHERE Variable_name LIKE \"wsrep%\";\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/processw')
def get_db_process_w(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \'select @@hostname\G SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/processr')
def get_db_process_r(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database-slave \'select @@hostname\G SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/indexercron')
def get_db_indexercron(project_id, environment):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -r database \"SELECT * FROM cron_schedule WHERE job_code LIKE 'indexer_%' LIMIT 100;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)