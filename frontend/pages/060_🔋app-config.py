import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def appconfig_backend_request(projid, envid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    if apiendpoint == 'files':
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/live/{projid}/{envid}/{apiparameter}")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[App Configuration] :battery:")


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Version", "Default URL", "Store Url", "CMS Url", "maintenance Status", "App Etc env.php"])

with tab1:
    st.header("Bin Magento Version (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Bin Magento Version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Default Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting app default url for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='defaulturl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Store Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting store url for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='storeurl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Cms Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting cms url for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='cmspageurl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Maintenance Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting maintenance status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='maintenance')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("App Etc ENV.php (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting env.php config file for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(apiendpoint='files',
                                             projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             apiparameter='app/etc/env.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
