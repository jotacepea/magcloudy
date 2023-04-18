import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[DB] :thread:")


tab1, tab2, tab3 = st.tabs(
    ["Db Version", "Db Size", "Db Process"])

with tab1:
    st.header("DB Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading DB version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/version")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

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
            st.write(f" ```{response.text}``` ")
with tab3:
    st.header("DB Process")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB process list for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"http://backend:5000/db/{st.session_state.projectid}/{st.session_state.environmentid}/process")
        print(response)
        if response:
            st.write(f" ```{response.text}``` ")

theend()
