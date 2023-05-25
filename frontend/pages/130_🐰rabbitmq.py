import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def rabbitmq_backend_request(projid, envid, apiendpoint='rabbitmq', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type == 'containerized' and apiendpoint == 'rabbitmq':
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[RabbitMQ] :rabbit:")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Rabbit Version", "Rabbit Info", "Rabbit Queues", "App Consumers", "Rabbit Healthchecks"])

with tab1:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Get Rabbit Version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            apiparameter='show')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("Queues")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Queues for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            apiparameter='listqueues')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
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

with tab4:
    st.header("Healthchecks")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Healthchecks for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            apiparameter='healthchecks')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
