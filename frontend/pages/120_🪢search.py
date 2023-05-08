import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def rabbitmq_backend_request(projid, envid, apiendpoint='opensearch', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type == 'containerized':
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}?containerized=1")
    else:
        resp = requests.get(
            f"http://backend:5000/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[OpenSearch] :knot:")
st.caption("**_In older versions could be ElasticSearch_**")

tab1, tab2, tab3 = st.tabs(
    ["Opensearch Version", "Opensearch Health", "Opensearch Indices"])

with tab1:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Get Rabbit Version for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Health")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
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
with tab3:
    st.header("Indices")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting RabbitMQ Queues for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apiparameter='indices')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
