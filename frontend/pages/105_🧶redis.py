import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def redis_backend_request(projid, envid, apiendpoint='redis', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'ping'
    if st.session_state.env_target_type.lower() == 'containerized':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Redis] :yarn:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
    st.info(f"**magento-cloud redis -p {st.session_state.projectid} -e {st.session_state.environmentid} -r redis INFO**")
    if st.session_state.env_target_type.lower() != 'containerized':
        st.info(f"**magento-cloud redis -p {st.session_state.projectid} -e {st.session_state.environmentid} -r redis-slave INFO**")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Redis Check",
     "Redis Server Info",
     "Redis Info",
     "Redis BigK",
     "Redis MemK",
     "Redis HotK"])

with tab1:
    st.header("Ping")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Check Redis for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Server Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Server Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='sinfo')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='info')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Big Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='bigkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Mem Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='memkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Hot Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='hotkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
