import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def search_backend_request(projid, envid, appid, apiendpoint='opensearch', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type.lower() == 'containerized':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

@st.cache_data(ttl=120)
def appconfig_backend_request(projid, envid, appid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

@st.cache_data(ttl=120)
def ssh_backend_request(projid, envid, appid, apiendpoint='ssh', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[OpenSearch] :knot:")
st.caption("**_In older versions could be ElasticSearch_**")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Search Engine",
     "Opensearch Version",
     "Opensearch Health",
     "Openserch Indices",
     "Opensearch Heap"])

with tab1:
    st.header("Search Engine Defined")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting magento search engine defined for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = appconfig_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid,
                                             apiparameter='searchengine')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Get Opensearch Version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid,
                                       appid=st.session_state.envappid)
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
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Health")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Opensearch Health for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = search_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='health')
        if response:
            for indx, openhealthline in enumerate(response.text.strip().split('\n')):
                if 'status' in openhealthline:
                    openhealthline = openhealthline.replace("\"", "")
                    openhealthline = openhealthline.replace(" ", "")
                    openhealthline = openhealthline.replace(",", "")
                    print(openhealthline)
                    openhealthvalues = openhealthline.strip().split(':')
                    print(openhealthvalues)
                    if openhealthvalues[1] == 'green':
                        st.success("**Cluster in Green State!**", icon="✅")
                    else:
                        if openhealthvalues[1] == 'yellow':
                            st.warning("**Cluster in Yellow State**", icon="🚧")
                        else:
                            st.error("**Cluster in Red State!**", icon="⛑️")
                            
                    # Warning: becuase of split... brackets already there.
                    mkdbody = f":{openhealthvalues[1]}{openhealthvalues}"
                    print(mkdbody)
                    st.markdown(mkdbody)
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab4:
    st.header("Indices")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Opensearch Indices for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = search_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='indices')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Heap")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Opensearch Heap for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = search_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='heap')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
