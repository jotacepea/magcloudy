import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


st.header("MagCloudy :blue[Crons] :timer_clock:")


tab1, tab2 = st.tabs(
    ["Cron Tab", "Cron List"])

with tab1:
    st.header("Indexer Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting magento indexer status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")


with tab2:
    st.header("Indexer Cron Status (**Live**)")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting magento indexer cron status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")



theend()
