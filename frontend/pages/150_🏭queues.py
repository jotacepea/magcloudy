import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Queues] :factory:")

tab1, tab2, tab3 = st.tabs(
    ["DB Queues",
     "DB Queue Messages",
     "DB Queues Status"])

with tab1:
    st.header("Queues")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading db queues for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")


with tab2:
    st.header("Messages")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting messages info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")



with tab3:
    st.header("Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting message status log for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")


theend()
