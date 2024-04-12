import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def rabbitmq_backend_request(projid, envid, apiendpoint='rabbitmq', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type.lower() == 'containerized' and apiendpoint == 'rabbitmq':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Consumers] :loop:")

tab1, tab2 = st.tabs(
    ["Consumers",
     "Consumers Cron"])

with tab1:
    st.header("Consumers")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting App Consumers for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(apiendpoint='binmagento',
                                            projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            apiparameter='consumers')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Cron Execution Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting message status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/consumerercron")
        print(response)
        if response:
            code_query_line="SELECT count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages FROM cron_schedule WHERE job_code LIKE 'consumers%' AND DATE(created_at) > DATE(CURDATE() - 5) GROUP BY status, job_code;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")
        
theend()
