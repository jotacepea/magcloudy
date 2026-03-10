import streamlit as st
import requests
import json
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def environments_backend_request(projid, apiendpoint='environments', envid=None, apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
        if envid is None:
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")

    print(resp)
    return resp

st.header("MagCloudy :blue[Environments] :card_index:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
    st.info(f"**magento-cloud environments -p {st.session_state.projectid} -I -c +created,machine_name,updated**")

tab1, tab2, tab3 = st.tabs(
    ["Environments",
     "Env Info",
     "Env Topology"])

with tab1:
    st.header("All Environments")
    if st.session_state.projectid != 'noprojid':
        st.write(f"From project _{st.session_state.projectid}_")
        def parse_envs_info(envs_json_info):
            try:
                # Parse the entire JSON list
                data_list = json.loads(envs_json_info)
                if isinstance(data_list, list):
                    envs_table = []
                    for data in data_list:
                        if data.get('type', 'N/A') == 'production':
                            ptype = f"**:red[{data.get('type', 'N/A')}]**"
                        else:
                            if data.get('type', 'N/A') == 'staging':
                                ptype = f"**:blue[{data.get('type', 'N/A')}]**"
                            else:
                                ptype = data.get('type', 'N/A')
                        envs_table.append({
                            "ID": data.get('id', 'N/A'),
                            "Name": data.get('name', 'N/A'),
                            "Title": data.get('title', 'N/A'),
                            "Type": ptype,
                            "Last Active": data.get('last_active_at', 'N/A')
                        })
                    if envs_table:
                        st.table(envs_table)
                    else:
                        st.warning("No environment data found.")
                else:
                    st.warning("Expected a JSON list of environments.")
            except Exception as e:
                st.error(f"Error parsing environment JSON: {e}")
                st.code(envs_json_info)

        if not st.session_state.get('environments_cached_full'):
            response = environments_backend_request(
                projid=st.session_state.projectid
            )
            if response:
                st.session_state.environments_cached_full = response.text.strip()
        
        parse_envs_info(st.session_state.environments_cached_full)
        with st.expander("Show All Environments (raw)"):
            st.code(st.session_state.environments_cached_full, language='json')

with tab2:
    st.header("Environment Info")
    if not st.session_state.get('environments_cached'):
        response_list = environments_backend_request(
            projid=st.session_state.projectid,
            envid='pipe')
        if response_list:
            environments_list = []
            for indx, branchesinfoline in enumerate(response_list.text.strip().split('\n')):
                print(branchesinfoline)
                environments_list.append(branchesinfoline)
            print(environments_list)
    else:
        print(st.session_state.environments_cached)
        environments_list = st.session_state.environments_cached

    environment_id_input = st.selectbox(
        "Would you like to get environment info? (please, select one of those...)",
        environments_list,
        index=environments_list.index(st.session_state.environmentid) if st.session_state.environmentid != 'noenvid' else None,
        placeholder="Select project ENV...",
    )

    if environment_id_input:
        st.session_state.environmentid = environment_id_input
        if 'environment_info' in st.session_state:
            del st.session_state.environment_info
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting info for Environment: **{environment_id_input}**")
            
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=st.session_state.environmentid, apiparameter='url')
        if response:
            st.write(
                f"### Cloud Env [URL]({response.text.strip()}) ###")
            
        response = environments_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            apiparameter='info'
        )
        if response:
            st.session_state.environment_info = response.json()
            try:
                env_data = response.json()
                deployment_target = env_data.get('deployment_target', '')

                if deployment_target == 'local':
                    st.session_state.env_target_type = 'containerized'
                    st.write(f" **Instances type:** :red[{st.session_state.env_target_type}] ")
                elif deployment_target:
                    st.session_state.env_target_type = 'Instances (Unified Cluster)'
                    st.write(f" **Instances type:** :blue[{st.session_state.env_target_type}] ")
            except Exception as e:
                st.error(f"Error parsing environment info JSON: {e}")

            # Show a table with environment info here
            if st.session_state.environment_info:
                envinfo = st.session_state.environment_info
                ds = envinfo.get('deployment_state', {})
                env_info_data = []

                # Adding fields one by one
                fields_to_vals = [
                    ("Project", envinfo.get('project', 'N/A')),
                    ("ID", envinfo.get('id', 'N/A')),
                    ("Name", envinfo.get('name', 'N/A')),
                    ("Title", envinfo.get('title', 'N/A')),
                    ("Type", envinfo.get('type', 'N/A')),
                    ("Parent", envinfo.get('parent', 'N/A')),
                    ("Status", envinfo.get('status', 'N/A')),
                    ("HTTP Access Enabled",
                     str(envinfo.get('http_access', {}).get('is_enabled', 'N/A'))),
                    ("Enable SMTP", str(envinfo.get('enable_smtp', 'N/A'))),
                    ("Restrict Robots",
                     str(envinfo.get('restrict_robots', 'N/A'))),
                    ("Crons", str(ds.get('crons', 'N/A'))),
                    ("Created At", envinfo.get('created_at', 'N/A')),
                    ("Updated At", envinfo.get('updated_at', 'N/A')),
                    ("Last Active At", envinfo.get('last_active_at', 'N/A')),
                    ("Last Deployment At", ds.get('last_deployment_at', 'N/A'))
                ]

                for field, val in fields_to_vals:
                    env_info_data.append({"Field": field, "Value": val})

                st.table(env_info_data)

            with st.expander("Show Environment Info (raw)"):
                st.code(response.text.strip(), language='json')

with tab3:
    st.header("Environment Topology")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.info(f"**magento-cloud project:curl -p {st.session_state.projectid} /environments/{st.session_state.environmentid}/deployments | jq '.[1]'**")
        response = environments_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            apiparameter='envtopology'
        )
        if response:
            st.session_state.environment_topology = response.json()
            webapps = st.session_state.environment_topology.get('webapps', {})
            app_list = list(webapps.keys())
            print('app_list: ', app_list)
            numberapps = len(app_list)
            if numberapps > 1:
                st.warning(
                    "**More than One App running in this Env...**",
                    icon="🚧"
                )
                st.write(" ```\n" + "\n".join(app_list) + "\n``` ")
                st.warning(
                    f"**Right now, we will use the first one as default:** {app_list[0]}"
                    "\n\n\n"
                    "**But you can change it later (in apps info)**"
                )
                st.session_state.envappid = app_list[0]
            elif numberapps == 1:
                st.session_state.envappid = app_list[0]
            else:
                st.session_state.envappid = "AppsIdErrorAppsIdErrorAppsIdErrorAppsIdError"
            with st.expander("Show Environment Topology (raw)"):
                st.code(json.dumps(st.session_state.environment_topology, indent=2), language='json')

theend()
