import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def appconfig_backend_request(projid, envid, appid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    if apiendpoint == 'db':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Consumers] :loop:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info("**php bin/magento queue\:consumers\:list**")

tab1, tab2 = st.tabs(
    ["Consumers",
     "Consumers Cron"])

with tab1:
    st.header("Consumers")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting App Consumers for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='consumers')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Cron Consumers Execution Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting message status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiendpoint='db',
                                             apiparameter='consumerercron')
        print(response)
        if response:
            code_query_line="SELECT count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages FROM cron_schedule WHERE job_code LIKE 'consumers%' AND DATE(created_at) > DATE(CURDATE() - 5) GROUP BY status, job_code;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")
        
theend()
