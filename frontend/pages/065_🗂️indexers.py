import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def appconfig_backend_request(projid, envid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    if apiendpoint == 'db':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[App Indexers] :card_index_dividers:")


tab1, tab2 = st.tabs(
    ["Mage Indexer", "Mage Indexer Cron"])

with tab1:
    st.header("Indexer Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting magento indexer status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='indexer')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Indexer Cron Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting magento indexer cron status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             apiendpoint='db',
                                             apiparameter='indexercron')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")


theend()
