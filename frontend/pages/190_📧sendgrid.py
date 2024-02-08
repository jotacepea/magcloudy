import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def sendgrid_backend_request(projid, envid, apiendpoint='sendgrid', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        if st.session_state.env_target_type.lower() == 'containerized':
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/magentocloud-{envid}/{apiparameter}")
        else:
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/mece-{envid}/{apiparameter}")
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

st.header("MagCloudy :blue[SendGrid] :e-mail:")

st.caption(
    f"[ExperienceLeague SendGrid](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/project/sendgrid.html) // \
    [Adobe Commerce Cloud SendGrid API](https://wiki.corp.adobe.com/display/ACCOPS/Sendgrid+API+Commands)")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    ["SendGrid Search",
     "SendGrid Info",
     "SendGrid Domains",
     "SendGrid Stats",
     "SendGrid Credit",
     "SendGrid Bounce",
     "SendGrid Dropped",
     "SendGrid Messages Get",
     "SendGrid Messages History",
     "SendGrid Blocklist"])

with tab1:
    st.header("SendGrid Accounts")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid accounts for: **{st.session_state.projectid}**")
        response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("SendGrid Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        pcresponse = ssh_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            apiendpoint='ssh/platformcluster',
                                            apiparameter=0)
        if pcresponse:
            pcresponse_platformcluster = pcresponse.text.strip().replace('"', '')
            st.write(f" Platform Cluster name Env Var value: ```{pcresponse_platformcluster.strip()}``` ")
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='info')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("SendGrid Domains")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid domains info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='domains')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("SendGrid Stats")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid stats for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='stats')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("SendGrid Credit")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid credit info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='credit')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("SendGrid Bounce")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid bounce info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='bounce')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("SendGrid Dropped")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid dropped info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='dropped')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("SendGrid Msg Get")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid messages info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='msgget')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab9:
    st.header("SendGrid Msg History")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid messages info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='msghist')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab10:
    st.header("SendGrid Blocklist")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid blocklist info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=pcresponse_platformcluster.strip(), apiparameter='blocklist')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
