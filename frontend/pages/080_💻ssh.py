import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def ssh_backend_request(projid, envid, apiendpoint='ssh'):
    resp = requests.get(
        f"http://backend:5000/{apiendpoint}/{projid}/{envid}")
    print(resp)
    return resp


st.header("MagCloudy :blue[Secure Shell] :computer:")


tab1, tab2 = st.tabs(
    ["SSH CMD", "SSH CLI"])

with tab1:
    st.header("Instances")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading config file for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid)
        if response:
            for inst in response.text.strip().split():
                st.write(f" ```ssh {inst}``` ")

with tab2:
    st.header("Instances")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading config file for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid)
        if response:
            if len(response.text.strip().split()) == 1:
                st.write(
                    f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid}``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(
                        f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -I {indx + 1}``` ")

theend()
