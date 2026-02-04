import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=180)
def ssh_backend_request(projid, envid, appid, apiendpoint='ssh', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

@st.cache_data(ttl=180)
def appconfig_backend_request(projid, envid, appid, apiendpoint='binmagento', apiparameter=None):
    if apiparameter == None:
        apiparameter = 'version'
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{appid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[Web] :spider_web:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    response = appconfig_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiparameter='defaulturl')
    if response:
        print(response)
        storedefaulturl = response.text.strip()

    storedefaulturl_parts = storedefaulturl.split('/')
    print(storedefaulturl_parts)
    print(storedefaulturl_parts[2])

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':

    privatewebport = '8080'
    if st.session_state.env_target_type.lower() == 'containerized':
        privatewebport = '80'

    st.info(f"""
        **curl -sI \"{storedefaulturl}\" -A \"tatata-agent\" \
            -H \"Fastly-Debug: True\" -H \"Fastly-No-Shield: 1\" \
            -H \"X-Forwarded-Proto: https\" -H \"Host: {storedefaulturl_parts[2]}\"**
        """)
    st.info(f"""
        **curl -LSsD - -o /dev/null \"{storedefaulturl}\" \
            -H \"Content-Type: application/json\" -A \"tatata-agent\" \
            -H \"Fastly-Debug: True\" -H \"Fastly-No-Shield: 1\" \
            -H \"X-Forwarded-Proto: https\" -H \"Host: {storedefaulturl_parts[2]}\" \
            -d \'{{ \"query\": \"mutation {{ createEmptyCart }}\" }}\'**
        """)
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \
            \'curl -sI "http://localhost:{privatewebport}/" -H "X-Forwarded-Proto: https" -H "Host: {storedefaulturl_parts[2]}" \
            -A "tatata-agent" \'**
        """)
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \
            \'curl -sI "http://localhost:{privatewebport}/static/deployed_version.txt" -H "X-Forwarded-Proto: https" -H "Host: {storedefaulturl_parts[2]}" \
            -A "tatata-agent" \'**
        """)
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \
            \'curl -sI "http://localhost:{privatewebport}/checkout/cart/" -H "X-Forwarded-Proto: https" -H "Host: {storedefaulturl_parts[2]}" \
            -A "tatata-agent" \'**
        """)
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -I 1\
            \'curl -sI "http://localhost:{privatewebport}/health_check.php" -H "X-Forwarded-Proto: https" -H "Host: {storedefaulturl_parts[2]}" \
            -A "tatata-agent" \'**
        """)
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -I 1\
            \'curl -sI "http://localhost:{privatewebport}/magento_version" -H "X-Forwarded-Proto: https" -H "Host: {storedefaulturl_parts[2]}" \
            -A "tatata-agent" \'**
        """)

tab1, tab2, tab3 = st.tabs(
    ["Nginx Version"
     "Nginx Check",
     "Nginx Server Info",
     "Nginx Server Names"])

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    response_instances = ssh_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid)
    print(response_instances)

with tab1:
    st.header("Check")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Check Redis for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        if response_instances:
            st.caption(
                f"Local Forward Port Nginx/Web:")
            if len(response_instances.text.strip().split()) == 1:
                st.write(
                    f" ```ssh -L 8080:localhost:8080 {response_instances.text.strip()}``` ")
                response = ssh_backend_request(
                    projid=st.session_state.projectid,
                    envid=st.session_state.environmentid,
                    appid=st.session_state.envappid,
                    apiendpoint='ssh/nginxsyntax',
                    apiparameter=0)
                if response:
                    st.write(f" ```\n{response.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response_instances.text.strip().split()):
                    st.write(
                        f" ```ssh -L 8080:localhost:8080 {inst}``` ")
                response = ssh_backend_request(
                    projid=st.session_state.projectid,
                    envid=st.session_state.environmentid,
                    appid=st.session_state.envappid,
                    apiendpoint='ssh/nginxsyntax',
                    apiparameter=1)
                if response:
                    st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Server Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Reading Nginx Server Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        if response_instances:
            if len(response_instances.text.strip().split()) == 1:
                st.write(
                    f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid}``` ")
                reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                  envid=st.session_state.environmentid,
                                                  appid=st.session_state.envappid,
                                                  apiendpoint='ssh/nginxlisten',
                                                  apiparameter=0)
                print(reqresponse)
                st.write(f" ```\n{reqresponse.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response_instances.text.strip().split()):
                    st.write(
                        f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -I {indx + 1}``` ")
                    reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                      envid=st.session_state.environmentid,
                                                      appid=st.session_state.envappid,
                                                      apiendpoint='ssh/nginxlisten',
                                                      apiparameter=indx + 1)
                    print(indx, inst, reqresponse)
                    st.write(f" ```\n{reqresponse.text.strip()}\n``` ")

with tab3:
    st.header("Server Names")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Reading Nginx Server Names Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        if response_instances:
            if len(response_instances.text.strip().split()) == 1:
                st.write(
                    f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid}``` ")
                reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                  envid=st.session_state.environmentid,
                                                  appid=st.session_state.envappid,
                                                  apiendpoint='ssh/nginxservername',
                                                  apiparameter=0)
                print(reqresponse)
                if reqresponse:
                    for indx, listenservname in enumerate(reqresponse.text.strip().split()):
                        st.write(f" ```\n{listenservname}\n``` ")
            else:
                for indx, inst in enumerate(response_instances.text.strip().split()):
                    st.write(
                        f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -I {indx + 1}``` ")
                    reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                      envid=st.session_state.environmentid,
                                                      appid=st.session_state.envappid,
                                                      apiendpoint='ssh/nginxservername',
                                                      apiparameter=indx + 1)
                    print(indx, inst, reqresponse)
                    if reqresponse:
                        for indx, listenservname in enumerate(reqresponse.text.strip().split()):
                            st.write(f" ```\n{listenservname}\n``` ")
theend()
