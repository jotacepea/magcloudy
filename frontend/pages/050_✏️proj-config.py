import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def projconfig_backend_request(projid, envid, apiendpoint='files', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Project Configuration] :pencil2:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info(f"**magento-cloud read -p {st.session_state.projectid} -e {st.session_state.environmentid} \
            '.magento/routes.yaml'**")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["Project Root",
     "Mage .app.",
     "Mage .env.",
     "Mage -vars-",
     "Mage -config-",
     "Mage services",
     "Mage routes",
     "Mage php.ini"])

with tab1:
    st.header("Repo files in Project (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Read file .magento.app.yaml (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento.app.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Read file .magento.env.yaml (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento.env.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Read file magento-vars.php (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='magento-vars.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Read file config.php (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='app/etc/config.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Read file .magento/services.yaml (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        st.caption(
            "**Note:** this config file is applied on containerized environments only :bricks:")
        st.caption(
            "**Note:** for Prod production and for Prod staging kind of environments... verify services and versions installed!")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento/services.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("Read file .magento/routes.yaml (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento/routes.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("Read file php.ini (**Git-Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='php.ini')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
