import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def ssh_backend_request(projid, envid, apiendpoint='ssh', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Disk Usage] :floppy_disk:")


tab1, tab2, tab3 = st.tabs(
    ["Disk",
     "Mounts",
     "Free"])

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
    response_instances = ssh_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid)
    print(response_instances)

with tab1:
    st.header("Disk Usage per Instance")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting disk usage for: **{st.session_state.projectid}** in **{st.session_state.environmentid}** Instances")
        response = requests.get(
            f"{st.session_state.reqfqdn}/ssh/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            if len(response.text.strip().split()) == 1:
                st.write(f" ```HD Usage {response.text.strip().split()}``` ")
                response = requests.get(
                    f"{st.session_state.reqfqdn}/disk/{st.session_state.projectid}/{st.session_state.environmentid}")
                print(response)
                st.write(f" ```\n{response.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(f" ```HD Usage {inst}``` ")
                    response = requests.get(
                        f"{st.session_state.reqfqdn}/disk/{st.session_state.projectid}/{st.session_state.environmentid}/{indx + 1}")
                    print(indx, inst, response)
                    st.write(f" ```\n{response.text.strip()}\n``` ")
with tab2:
    st.header("Mounts Usage per Instance")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Mounts size for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/mounts/{st.session_state.projectid}/{st.session_state.environmentid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
        response = requests.get(
            f"{st.session_state.reqfqdn}/mounts/{st.session_state.projectid}/{st.session_state.environmentid}/size")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Mem Usage per Instance")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting memory usage for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if response_instances:
            if len(response_instances.text.strip().split()) == 1:
                st.write(
                    f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid}``` ")
                reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                  envid=st.session_state.environmentid,
                                                  apiendpoint='ssh/free',
                                                  apiparameter=0)
                print(reqresponse)
                st.write(f" ```\n{reqresponse.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response_instances.text.strip().split()):
                    st.write(
                        f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -I {indx + 1}``` ")
                    reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                      envid=st.session_state.environmentid,
                                                      apiendpoint='ssh/free',
                                                      apiparameter=indx + 1)
                    print(indx, inst, reqresponse)
                    st.write(f" ```\n{reqresponse.text.strip()}\n``` ")


theend()
