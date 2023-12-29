from apiflask import APIBlueprint
import subprocess
import os

newrelic_bp = APIBlueprint('newrelic-blueprint', __name__)


@newrelic_bp.get('/newrelic/<project_id>/<environment>')
def get_newrelic(project_id, environment):
    NR_GRAPHQL_QUERY="{ actor { user { name } } }"
    command_magecloud = f"newrelic-cli nerdgraph query '{NR_GRAPHQL_QUERY}'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@newrelic_bp.get('/newrelic/<project_id>/<environment>/account')
def get_newrelic_account(project_id, environment):
    NR_GRAPHQL_QUERY="""{
  actor {
    accounts {
      id
      name
    }
  }
}"""
    command_magecloud = f"newrelic-cli nerdgraph query '{NR_GRAPHQL_QUERY}' | grep -B1 '{project_id}'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud

@newrelic_bp.get('/newrelic/<project_id>/<nr_account_id>/transactions')
def get_newrelic_transactions(project_id, nr_account_id):
    NR_GRAPHQL_QUERY="""
query($my_nr_account_id: Int!)
{
   actor {
      account(id: $my_nr_account_id) {
         nrql(query: "FROM Transaction SELECT count(*) FACET appName") {
            results
         }
      }
   }
}
"""
    NR_GRAPHQL_QUERY_VARS=f"""
{{"my_nr_account_id":{nr_account_id}}}
"""
    command_magecloud = f"newrelic-cli nerdgraph query '{NR_GRAPHQL_QUERY}' --variables '{NR_GRAPHQL_QUERY_VARS}'"
    try:
        result_command_magecloud = subprocess.check_output(
            [command_magecloud], shell=True, env=os.environ, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to shell cmd: %s" % e

    return result_command_magecloud


