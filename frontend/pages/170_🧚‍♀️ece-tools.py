import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def ecetools_backend_request(projid, envid, appid, apiendpoint='ece-tools', apiparameter='version'):
    if envid is None:
        envid = 'master'
    if apiendpoint == 'variables' and apiparameter is None:
        apiparameter = 'p'
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[ECE-Tools] :fairy:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info("**php vendor/bin/ece-tools env\:config\:show**")
    st.info("**php vendor/bin/ece-patches status**")
    
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["ECE-Tools Version",
     "ECE-Tools Show Error",
     "ECE-Tools Show Env Config",
     "ECE-Tools Validate Cloud Config",
     "ECE-Tools Check Wizards",
     "ECE-Patches Status"])

with tab1:
    st.header("ECE Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Reading ece-tools version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        st.write("https://github.com/magento/ece-tools/releases")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("ECE Error")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting ece-tools last error for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='error')
        if response:
            for indx, ecetoolerrorline in enumerate(response.text.strip().split('\n')):
                if 'type:' in ecetoolerrorline:
                    ecetoolerrorline = ecetoolerrorline.replace(":", "")
                    print(ecetoolerrorline)
                    st.write(f" ```{ecetoolerrorline}``` ")
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("ECE Config")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting ece-tools env config for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='config')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("ECE Validate")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Validate ece-tools cloud config for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='validate')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("ECE Wizards")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Checking ece-tools wizards for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='wizards')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("ECE Patches")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Checking ece-tools patches for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ecetools_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='patches')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
