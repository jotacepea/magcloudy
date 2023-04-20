import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def rabbitmq_backend_request(projid, envid, apiendpoint='rabbitmq', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type == 'containerized':
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[RabbitMQ] :rabbit:")


tab1, tab2, tab3 = st.tabs(
    ["Rabbit Version", "Rabbit Info", "Rabbit Queues"])

with tab1:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Get Rabbit Version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid)
        if response:
            st.write(f" ```{response.text.strip()}``` ")

with tab2:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='show')
        if response:
            st.write(f" ```{response.text}``` ")
with tab3:
    st.header("Queues")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Queues for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='listqueues')
        if response:
            st.write(f" ```{response.text}``` ")

theend()
