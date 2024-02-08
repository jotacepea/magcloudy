import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def search_backend_request(projid, envid, apiendpoint='opensearch', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type.lower() == 'containerized':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

@st.cache_data(ttl=150)
def appconfig_backend_request(projid, envid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

@st.cache_data(ttl=60)
def ssh_backend_request(projid, envid, apiendpoint='ssh', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[OpenSearch] :knot:")
st.caption("**_In older versions could be ElasticSearch_**")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Search Engine",
     "Opensearch Version",
     "Opensearch Health",
     "Opensearch Indices"])

with tab1:
    st.header("Search Engine Defined")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting magento search engine defined for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             apiparameter='searchengine')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Get Opensearch Version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid)
        print(response)
        if response:
            st.caption(
                f"Local Forward Port OpenSearch Web API:")
            if len(response.text.strip().split()) == 1:
                st.write(
                    f" ```ssh -L 19200:opensearch.internal:9200 {response.text.strip()}``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(
                        f" ```ssh -L 19200:localhost:9200 {inst}``` ")
        st.write(st.session_state.env_target_type)
        response = search_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Health")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Opensearch Health for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = search_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='health')
        if response:
            for indx, openhealthline in enumerate(response.text.strip().split('\n')):
                if 'status' in openhealthline:
                    openhealthline = openhealthline.replace("\"", "")
                    openhealthline = openhealthline.replace(" ", "")
                    openhealthline = openhealthline.replace(",", "")
                    print(openhealthline)
                    openhealthvalues = openhealthline.strip().split(':')
                    print(openhealthvalues)
                    # Warning: becuase of split... brackets already there.
                    mkdbody = f":{openhealthvalues[1]}{openhealthvalues}"
                    print(mkdbody)
                    st.markdown(mkdbody)
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab4:
    st.header("Indices")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Opensearch Indices for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = search_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='indices')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
