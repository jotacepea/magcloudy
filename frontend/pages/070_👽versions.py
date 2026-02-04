import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Software Versions] :alien:")

st.caption(
    f"[System Requirements - Services version](https://experienceleague.adobe.com/en/docs/commerce-operations/installation-guide/system-requirements)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Magento Version", "ECE-Tools version", "PHP Version", "Nginx Version", "Backend Services"])

with tab1:
    st.header("magento")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Magento version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/versions/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/magento")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("ece-tools")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting ece-tools version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/ece-tools/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/version")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("php")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting php version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/versions/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/php")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("nginx")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting nginx version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/versions/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/nginx")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("services")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting env services definition for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        st.caption(
            f"**Note:** if :red[NOT] containerized environment... _please verify those versions!!!_")
        response = requests.get(
            f"{st.session_state.reqfqdn}/services/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
