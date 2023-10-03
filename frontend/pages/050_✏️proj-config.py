import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def projconfig_backend_request(projid, envid, apiendpoint='files', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[Project Configuration] :pencil2:")


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["Project Root", "Mage .app.", "Mage .env.", "Mage -vars-", "Mage -config-", "Mage services", "Mage routes", "Mage php.ini"])

with tab1:
    st.header("Repo files in Project (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Read file .magento.app.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento.app.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Read file .magento.env.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento.env.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Read file magento-vars.php (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='magento-vars.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Read file config.php (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='app/etc/config.php')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Read file .magento/services.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento/services.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("Read file .magento/routes.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='.magento/routes.yaml')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("Read file php.ini (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = projconfig_backend_request(projid=st.session_state.projectid,
                                              envid=st.session_state.environmentid, apiparameter='php.ini')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
