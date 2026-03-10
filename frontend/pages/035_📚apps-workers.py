import streamlit as st
import requests
import json
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def apps_backend_request(projid, envid, apiendpoint='apps', appid=None, apiparameter=None):
    if appid is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
        if apiparameter != None:
            resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")

    print(resp)
    return resp

st.header("MagCloudy :blue[Apps] :books:")

tab1, tab2 = st.tabs(
    ["Apps&Workers",
     "Apps&Workers Info"])

with tab1:
    st.header("All Apps&Workers")
    response = apps_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid
            )
    if response:
        st.code(response.text.strip(), language='yaml')

    if st.session_state.get('environment_topology'):
        envinfo = st.session_state.environment_topology
        webapps = envinfo.get('webapps', {})
        workers = envinfo.get('workers', {})
        
        apps_workers_data = []
        
        for name, config in webapps.items():
            apps_workers_data.append({
                "Type": "**Webapp**",
                "Name": name,
                "Instances": config.get('instance_count', 'N/A'),
                "Disk (MB)": config.get('disk', 'N/A')
            })
            
        for name, config in workers.items():
            apps_workers_data.append({
                "Type": "Worker",
                "Name": name,
                "Instances": config.get('instance_count', 'N/A'),
                "Disk (MB)": config.get('disk', 'N/A')
            })
            
        if apps_workers_data:
            st.table(apps_workers_data)
            if webapps:
                with st.expander("Show All Apps (raw)"):
                    st.code(json.dumps(webapps, indent=2), language='json')
            if workers:
                with st.expander("Show All Workers (raw)"):
                    st.code(json.dumps(workers, indent=2), language='json')
        else:
            st.warning("No Apps or Workers found in environment info.")
    else:
        st.warning("Environment info not loaded. Please visit the 'Environments' page first.")

with tab2:
    apps_list = []
    if st.session_state.get('environment_info'):
        envinfo = st.session_state.environment_info
        sizing = envinfo.get('sizing', {})
        apps_list = list(sizing.get('webapps', {}).keys())

    app_id_input = st.selectbox(
        "Would you like to get app info? (please, select one of those...)",
        apps_list,
        index=apps_list.index(st.session_state.envappid) if st.session_state.envappid in apps_list else None,
        placeholder="Select APP...",
    )

    if app_id_input and st.session_state.projectid != 'noprojid' and \
       st.session_state.environmentid != 'noenvid':
        msg = f"Getting App info for **{app_id_input}** in " \
              f"**{st.session_state.environmentid}** from " \
              f"**{st.session_state.projectid}**"
        st.write(msg)

        response = apps_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=app_id_input,
            apiparameter='config')
        if response:
            st.code(response.text.strip(), language='yaml')

theend()
