import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def rabbitmq_backend_request(projid, envid, appid, apiendpoint='rabbitmq', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'version'
    if st.session_state.env_target_type.lower() == 'containerized' and apiendpoint == 'rabbitmq':
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}?containerized=1")
    else:
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

st.header("MagCloudy :blue[RabbitMQ] :rabbit:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    if st.session_state.env_target_type.lower() == 'containerized':
        st.info(f"""
                **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \'curl -u guest:guest -sk http://rabbitmq.internal:15672/api/queues | json_pp | grep name\'**
            """)
    else:
        st.info(f"""
                **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \'curl -u $USER -sk http://localhost:15672/api/queues | jq -r .[].name\'**
            """)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Rabbit Version",
     "Rabbit Info",
     "Rabbit Queues",
     "Rabbit Healthchecks"])

with tab1:
    st.header("Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Get Rabbit Version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid,
                                       appid=st.session_state.envappid)
        print(response)
        if response:
            st.caption(
                f"Local Forward Port MQP UI:")
            if len(response.text.strip().split()) == 1:
                st.write(
                    f" ```ssh -L 15672:rabbitmq.internal:15672 {response.text.strip()}``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(
                        f" ```ssh -L 15672:localhost:15672 {inst}``` ")

        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting RabbitMQ Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='show')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("Queues")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting RabbitMQ Queues for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='listqueues')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Healthchecks")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting RabbitMQ Healthchecks for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = rabbitmq_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='healthchecks')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
