import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def environments_backend_request(projid, apiendpoint='environments', envid=None, apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}")
        if envid is None:
            resp = requests.get(
                f"http://backend:5000/{apiendpoint}/{projid}")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")

    print(resp)
    return resp


st.header("MagCloudy :blue[Environments] :card_index:")


tab1, tab2 = st.tabs(["Environments", "Env Info"])

with tab1:
    st.header("All Environments")
    if st.session_state.projectid != 'noprojid':
        st.write(f"_{st.session_state.projectid}_")
        response = environments_backend_request(
            projid=st.session_state.projectid)
        if response:
            st.write(f" ```{response.text}``` ")

with tab2:
    st.header("Environment Info")
    environment_id_input = st.text_input(
        "Enter some environment name 👇",
        value=st.session_state.environmentid if st.session_state.environmentid != 'noenvid' else '',
        placeholder="staging",
    )
    if environment_id_input:
        st.session_state.environmentid = environment_id_input
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write("Getting info for Environment: ", environment_id_input)
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=environment_id_input, apiparameter='url')
        if response:
            st.write(f"Cloud Env URL {response.text}")
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=environment_id_input, apiparameter='info')
        if response:
            for indx, envinfoline in enumerate(response.text.strip().split('\n')):
                if 'deployment_target' in envinfoline:
                    envinfoline = envinfoline.replace("|", "")
                    print(envinfoline)
                    st.write(f" ```{envinfoline}``` ")
            st.write(f" ```{response.text}``` ")

theend()
