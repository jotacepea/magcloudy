import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Info Page]! :nazar_amulet:")

tab1, tab2, tab3 = st.tabs(["Version", "Auth", "List"])

with tab1:
    st.header("MagCloudy: Cli Version")
    response = requests.get(f"{st.session_state.reqfqdn}/mgcliversion")
    print(response)
    st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("MagCloudy: Cli Auth Info")
    response = requests.get(f"{st.session_state.reqfqdn}/mgcliauth")
    print(response)
    st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("MagCloudy: Cli Cmd List")
    response = requests.get(f"{st.session_state.reqfqdn}/mgclilist")
    print(response)
    st.write(f" ```\n{response.text.strip()}\n``` ")

theend(enable_select_proj_env_warning = False)