import streamlit as st
import requests
import json
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
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
        if st.session_state.projectid != 'noprojid':
            st.header("All Environments")
            st.write(f"From project **_{st.session_state.projectid}_**")
            def parse_envs_info(envs_json_info):
                try:
                    # Parse the entire JSON list
                    data_list = json.loads(envs_json_info)
                    if isinstance(data_list, list):
                        envs_table = []
                        for data in data_list:
                            if data.get('status', 'N/A') == 'active':
                                status = f"**:grey[{data.get('status', 'N/A')}]**"
                            else:
                                status = f"**:red[{data.get('status', 'N/A')}]**"
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
                                "Last Active": data.get('last_active_at', 'N/A'),
                                "Status": status,
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
        if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
            st.header("Environment Info")
            st.write(f"Getting info for Environment: **{st.session_state.environmentid}**")
            
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
        if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
            st.header("Environment Topology")
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
            
                # WebApp Display info 
                webapps = st.session_state.environment_topology.get('webapps', {})
                if webapps:
                    st.subheader(":grey[Env WebApps:]")
                    for webapp_name, webapp_info in webapps.items():
                        st.subheader(f"**{webapp_name}** ({webapp_info.get('type', 'N/A')})", divider=True)
                        dependencies = webapp_info.get('dependencies', {})
                        if dependencies:
                            st.write("**Dependencies:**")
                            for dep_name, dep_info in dependencies.items():
                                st.write(f"- {dep_name}:\n {dep_info}")
                        else:
                            st.write("No dependencies found for this service.")

                # Services Display Logic
                services = st.session_state.environment_topology.get('services', {})
                if services:
                    st.subheader(":grey[Env Services:]")
                    for service_name, service_info in services.items():
                        st.subheader(f"**{service_name}** ({service_info.get('type', 'N/A')})", divider=True)
                        endpoints = service_info.get('endpoints', {})
                        if endpoints:
                            st.write("**Endpoints:**")
                            for ep_name, ep_info in endpoints.items():
                                scheme = ep_info.get('scheme', 'N/A')
                                port = ep_info.get('port', 'N/A')
                                st.write(f"- `{ep_name}`: `{scheme}://{port}`")
                        else:
                            st.write("No endpoints found for this service.")

                with st.expander("Show Environment Topology (raw)"):
                    st.code(json.dumps(st.session_state.environment_topology, indent=2), language='json')

theend()
