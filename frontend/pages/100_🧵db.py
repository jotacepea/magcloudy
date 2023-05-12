import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[DB] :thread:")


tab1, tab2, tab3, tab4 = st.tabs(
    ["Db Version", "Db Size", "Db Process", "Cluster Status"])

with tab1:
    st.header("DB Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading DB version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/version")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("DB Size")
    st.caption(
        "**Note:** this section works for containerized environments only :bricks:)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB size for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/size")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("DB Process")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB process list for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/processw")
        print(response)
        if response:
            st.write("Write connection...")
            st.write(f" ```\n{response.text.strip()}\n``` ")
        if st.session_state.env_target_type != 'containerized':
            response = requests.get(
                f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/processr")
            print(response)
            if response:
                st.write("Read connection...")
                st.write(f" ```\n{response.text.strip()}\n``` ")
with tab4:
    st.header("DB Cluster Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type != 'containerized':
        st.write(
            f"Getting DB cluster status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/wsrep")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        st.write(f"No DB Cluster info --> {st.session_state.env_target_type}")

theend()
