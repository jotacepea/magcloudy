import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def redis_backend_request(projid, envid, apiendpoint='redis', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'ping'
    resp = requests.get(
        f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[Redis] :yarn:")


tab1, tab2, tab3 = st.tabs(
    ["Redis Check", "Redis Server Info", "Redis Info"])

with tab1:
    st.header("Ping")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Check Redis for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid)
        if response:
            st.write(f" ```{response.text.strip()}``` ")

with tab2:
    st.header("Server Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Server Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='sinfo')
        if response:
            st.write(f" ```{response.text}``` ")
with tab3:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='info')
        if response:
            st.write(f" ```{response.text}``` ")

theend()
