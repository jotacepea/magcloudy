import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Project Configuration] :pencil2:")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Project Root", "Mage .app.", "Mage .env.", "Mage -vars-", "Mage -config-"])

with tab1:
    st.header("Repo files in Project (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/files/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

with tab2:
    st.header("Read file .magento.app.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/files/{st.session_state.projectid}/{st.session_state.environmentid}/.magento.app.yaml")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

with tab3:
    st.header("Read file .magento.env.yaml (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/files/{st.session_state.projectid}/{st.session_state.environmentid}/.magento.env.yaml")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

with tab4:
    st.header("Read file magento-vars.php (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/files/{st.session_state.projectid}/{st.session_state.environmentid}/magento-vars.php")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

with tab5:
    st.header("Read file config.php (**Repos**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting project **repos** files for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/files/{st.session_state.projectid}/{st.session_state.environmentid}/app/etc/config.php")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

theend()
