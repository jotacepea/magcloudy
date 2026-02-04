import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=180)
def appconfig_backend_request(projid, envid, appid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    if apiendpoint == 'files':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/live/{projid}/{envid}/{appid}/{apiparameter}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[App Configuration] :battery:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info("**php bin/magento config\:show\:default-url**")
    st.info("**php bin/magento maintenance\:status**")
    st.info("**php bin/magento store\:list -n**")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    ["Version",
     "Default URL",
     "Store Url",
     "CMS Url",
     "Admin Url",
     "Maintenance Status",
     "App Etc env.php",
     "Websites",
     "Stores"])

with tab1:
    st.header("Bin Magento Version (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Bin Magento Version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Default Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting app default url for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='defaulturl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Store Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting store url for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='storeurl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Cms Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting cms url for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='cmspageurl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Admin Url (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting admin url for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='adminurl')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='adminurlcustom')
        if response:
            st.write("Store Admin Url Custom Path (if defined):")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Maintenance Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting maintenance status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='maintenance')
        if response:
            for indx, mstatusline in enumerate(response.text.strip().split('\n')):
                if 'Status' in mstatusline:
                    if 'not' or 'disabled' in mstatusline:
                        st.success("**Maintenance mode Off!**", icon="✅")
                    else:
                        st.error("**Maintenance Enabled!**", icon="🚨")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("App Etc ENV.php (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting env.php config file for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(apiendpoint='files',
                                             projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='app/etc/env.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("Websites (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting websites for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='websites')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab9:
    st.header("Stores (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting stores for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='stores')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
