import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def environments_backend_request(projid, apiendpoint='environments', envid=None, apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
        if envid is None:
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")

    print(resp)
    return resp

st.header("MagCloudy :blue[Environments] :card_index:")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Environments",
     "Env Info",
     "Env Config Smtp State",
     "Env Config Crons State"])

with tab1:
    st.header("All Environments")
    if st.session_state.projectid != 'noprojid':
        st.write(f"From project _{st.session_state.projectid}_")
        response = environments_backend_request(
            projid=st.session_state.projectid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Environment Info")
    response_list = environments_backend_request(
        projid=st.session_state.projectid,
        envid='pipe')
    if response_list:
        environments_list = []
        for indx, branchesinfoline in enumerate(response_list.text.strip().split('\n')):
            print(branchesinfoline)
            environments_list.append(branchesinfoline)
        print(environments_list)

    environment_id_input = st.selectbox(
        "Would you like to get environment info? (please, select one of those...)",
        environments_list,
        index=environments_list.index(st.session_state.environmentid) if st.session_state.environmentid != 'noenvid' else None,
        placeholder="Select project ENV...",
    )

    # environment_id_input = st.text_input(
    #     "Enter some environment name 👇",
    #     value=st.session_state.environmentid if st.session_state.environmentid != 'noenvid' else '',
    #     placeholder="staging",
    # )
    if environment_id_input:
        st.session_state.environmentid = environment_id_input
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting info for Environment: **{environment_id_input}**")
            
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=st.session_state.environmentid, apiparameter='url')
        if response:
            st.write(
                f"### Cloud Env [URL]({response.text.strip()}) ###")
            
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=st.session_state.environmentid, apiparameter='info')
        if response:
            appresponse = requests.get(
            f"{st.session_state.reqfqdn}/apps/{st.session_state.projectid}/{environment_id_input}/pipe")
            print(appresponse.text)
            numberapps=len(appresponse.text.strip().split('\n'))
            print(numberapps)
            if numberapps > 1:
                st.warning("**More than One App running in this Env...**", icon="🚧")
                st.write(f" ```\n{appresponse.text.strip()}\n``` ")
            else:
                if numberapps == 1:
                    st.session_state.envappid = appresponse.text.strip()
                else:
                    st.session_state.envappid = "AppsIdErrorAppsIdErrorAppsIdErrorAppsIdError"

            for indx, envinfoline in enumerate(response.text.strip().split('\n')):
                if 'deployment_target' in envinfoline:
                    envinfoline = envinfoline.replace("|", "")
                    print(envinfoline)
                    #st.write(f" ```{envinfoline}``` ")
                    if 'local' in envinfoline:
                        st.session_state.env_target_type = 'containerized'
                        st.caption(f"**_{st.session_state.env_target_type}_**")
                    else:
                        st.session_state.env_target_type = 'Instances (Unified Cluster)'
                        st.caption(f"**_{st.session_state.env_target_type}_**")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Smtp State")
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting smtp config for environment: **{st.session_state.environmentid}**")
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=st.session_state.environmentid, apiparameter='enablesmtpstatus')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Crons State")
    if environment_id_input and st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting smtp config for environment: **{st.session_state.environmentid}**")
        response = environments_backend_request(projid=st.session_state.projectid,
                                                envid=st.session_state.environmentid, apiparameter='deploymentstatecrons')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
