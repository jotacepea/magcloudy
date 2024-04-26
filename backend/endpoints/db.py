from apiflask import APIBlueprint
import subprocess
import os
from strip_ansi import strip_ansi

db_bp = APIBlueprint('db-blueprint', __name__)


@db_bp.get('/db/<project_id>/<environment>/<appid>/version')
def get_db_version(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \'SELECT VERSION();\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/size')
def get_db_size(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:size -p {project_id} -e {environment} -A {appid} -r database"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/status')
def get_db_status(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \'status;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/tablesize')
def get_db_tablesize(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \'SELECT table_schema as `Database`, table_name AS `Table`, ROUND(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` FROM information_schema.TABLES ORDER BY (data_length + index_length) DESC LIMIT 15;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/myisam')
def get_db_myisam(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE engine = 'MyISAM' AND TABLE_SCHEMA <> 'mysql';\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/primarykey')
def get_db_primarykey(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"SELECT table_schema, table_name, engine, 'NoPrimKey!!!' FROM information_schema.tables WHERE (table_schema, table_name) NOT IN (SELECT table_schema, table_name FROM information_schema.table_constraints  WHERE constraint_type = 'PRIMARY KEY') AND table_schema NOT IN ('information_schema', 'pg_catalog');\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/wsrep')
def get_db_wsrep(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \'SHOW STATUS WHERE Variable_name LIKE \"wsrep%\";\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/processw')
def get_db_process_w(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \'select @@hostname\G SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)


@db_bp.get('/db/<project_id>/<environment>/<appid>/processr')
def get_db_process_r(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database-slave \'select @@hostname\G SHOW PROCESSLIST;\'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/indexercron')
def get_db_indexercron(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages from cron_schedule where job_code like 'indexer%' and DATE(created_at) > DATE(CURDATE() - 5) group by status, job_code;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/consumerercron')
def get_db_consumercron(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages from cron_schedule where job_code like 'consumers%' and DATE(created_at) > DATE(CURDATE() - 5) group by status, job_code;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/othercron')
def get_db_othercron(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages from cron_schedule where job_code NOT like 'consumers%' and job_code NOT like 'indexer%' and DATE(created_at) > DATE(CURDATE() - 5) group by status, job_code;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/cronlist')
def get_db_cronlist(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select job_code, created_at from cron_schedule group by job_code;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/queuelist')
def get_db_queuelist(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select id,name from queue;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/queuemessages')
def get_db_queuemessages(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select count(*) as Messages, topic_name from queue_message group by topic_name;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/queuemsgstatus')
def get_db_queuemsgstatus(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"SELECT count(*), topic_name, queue_id, updated_at, status FROM queue_message qm INNER JOIN queue_message_status qms ON qm.id = qms.message_id WHERE DATE(updated_at) > DATE(CURDATE() - 5) GROUP BY topic_name, status LIMIT 50;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)

@db_bp.get('/db/<project_id>/<environment>/<appid>/queuemsgtrials')
def get_db_queuemsgtrials(project_id, environment, appid):
    command_magecloud = f"magento-cloud db:sql -p {project_id} -e {environment} -A {appid} -r database \"select count(*), name, status, number_of_trials from queue_message_status s join queue q on s.queue_id = q.id WHERE DATE(updated_at) > DATE(CURDATE() - 5) GROUP BY status, name, number_of_trials LIMIT 50;\""
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return strip_ansi(result_command_magecloud)