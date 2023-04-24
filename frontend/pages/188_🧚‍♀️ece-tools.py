import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def ecetools_backend_request(projid, envid, apiendpoint='ece-tools', apiparameter='version'):
    if envid is None:
        envid = 'master'
    if apiendpoint == 'variables' and apiparameter is None:
        apiparameter = 'p'
    resp = requests.get(
        f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[ECE-Tools] :fairy:")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["ECE-Tools Version",
     "ECE-Tools Show Error",
     "ECE-Tools Show Env Config",
     "ECE-Tools Validate Cloud Config",
     "ECE-Tools Check Wizards"])

with tab1:
    st.header("ECE Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading ece-tools version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("ECE Error")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting ece-tools last error for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid, apiparameter='error')
        if response:
            for indx, ecetoolerrorline in enumerate(response.text.strip().split('\n')):
                if 'type:' in ecetoolerrorline:
                    ecetoolerrorline = ecetoolerrorline.replace(":", "")
                    print(ecetoolerrorline)
                    st.write(f" ```{ecetoolerrorline}``` ")
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("ECE Config")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting ece-tools env config for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid, apiparameter='config')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("ECE Validate")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Validate ece-tools cloud config for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid, apiparameter='validate')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("ECE Wizards")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Checking ece-tools wizards for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid, apiparameter='wizards')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
