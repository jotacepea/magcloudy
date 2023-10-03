import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def variables_backend_request(projid, apiendpoint='variables', envid=None, apiparameter=None):
    if envid is None:
        envid = 'master'
    if apiendpoint == 'variables' and apiparameter is None:
        apiparameter = 'p'
    resp = requests.get(
        f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[Environment Variables] :radioactive_sign:")


tab1, tab2, tab3 = st.tabs(
    ["Project Vars", "Environment Vars", "Env Relationships"])

with tab1:
    st.header("Env Variables at Project Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting Env Vars for:  **{st.session_state.projectid}**")
        response = variables_backend_request(projid=st.session_state.projectid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Env Variables at Environment Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Env Vars for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = variables_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='e')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Env Relationships at Environment Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Env Relationships values for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = variables_backend_request(apiendpoint='environments', projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apiparameter='relationships')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
