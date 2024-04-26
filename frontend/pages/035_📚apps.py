import streamlit as st
import requests
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
    ["Apps",
     "App Info"])

with tab1:
    st.header("All Apps")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Get Apps for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = apps_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("App Info")
    response_list = apps_backend_request(
        projid=st.session_state.projectid,
        envid=st.session_state.environmentid,
        apiparameter='pipe')
    if response_list:
        apps_list = []
        for indx, appsinfoline in enumerate(response_list.text.strip().split('\n')):
            print(appsinfoline)
            apps_list.append(appsinfoline)
        print(apps_list)

    app_id_input = st.selectbox(
        "Would you like to get app info? (please, select one of those...)",
        apps_list,
        index=apps_list.index(st.session_state.envappid) if st.session_state.envappid != 'noenvappid' else None,
        placeholder="Select APP...",
    )

    if app_id_input:
        st.session_state.envappid = app_id_input
    if app_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting App info for **{app_id_input}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
            
        response = apps_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=app_id_input,
            apiparameter='config')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
