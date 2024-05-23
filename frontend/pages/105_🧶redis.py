import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=120)
def redis_backend_request(projid, envid, appid, apiendpoint='redis', apiparameter=None):
    if apiparameter is None:
        apiparameter = 'ping'
    if st.session_state.env_target_type.lower() == 'containerized':
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

st.header("MagCloudy :blue[Redis] :yarn:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info(f"**magento-cloud redis -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r redis INFO**")
    if st.session_state.env_target_type.lower() != 'containerized':
        st.info(f"**magento-cloud redis -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r redis-slave INFO**")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["Redis Check",
     "Redis Server Info",
     "Redis Info",
     "Redis Lazy",
     "Redis BigK",
     "Redis MemK",
     "Redis HotK"])

with tab1:
    st.header("Ping")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Check Redis for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = ssh_backend_request(projid=st.session_state.projectid,
                                       envid=st.session_state.environmentid,
                                       appid=st.session_state.envappid)
        print(response)
        if response:
            st.caption(
                f"Local Forward Port Redis:")
            if len(response.text.strip().split()) == 1:
                st.write(
                    f" ```ssh -L 26379:redis.internal:26379 {response.text.strip()}``` ")
            else:
                for indx, inst in enumerate(response.text.strip().split()):
                    st.write(
                        f" ```ssh -L 26379:localhost:26379 {inst}``` ")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Server Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Server Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='sinfo')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
with tab3:
    st.header("Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='info')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Big Lazy")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Lazyfree-Lazy Server Config for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='lazyfreelazy')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Big Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='bigkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Mem Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='memkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("Hot Keys")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Redis Full Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = redis_backend_request(
            projid=st.session_state.projectid,
            envid=st.session_state.environmentid,
            appid=st.session_state.envappid,
            apiparameter='hotkeys')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
