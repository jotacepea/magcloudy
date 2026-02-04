import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=180)
def sendgrid_backend_request(projid, envid, apiendpoint='sendgrid', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
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

st.header("MagCloudy :blue[SendGrid] :e-mail:")

st.caption(
    f"[ExperienceLeague SendGrid](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/project/sendgrid.html) // \
    [Adobe Commerce Cloud SendGrid API](https://wiki.corp.adobe.com/display/ACCOPS/Sendgrid+API+Commands) // \
    [Overwatch](https://sendgrid.pltfrm.sh/docs/)")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info("**curl -sH \"Authorization: Bearer $(magento-cloud a\:t 2>/dev/null)\" 'https://magento-admin.sendgrid.pltfrm.sh/api/v1/sendgrid/info/me'**")
    st.info(f"**clush -LNw \$(magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} --all --pipe |\
            tr '\\n' ',' | rev | cut -c2- | rev) 'hostname;grep sendgrid /var/log/mail.log | tail'**")
    st.info(f"**clush -LNw \$(magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} --all --pipe |\
            tr '\\n' ',' | rev | cut -c2- | rev) 'env | grep -i MAGENTO_CLOUD_SMTP_HOST'**")
    st.info(f"**magento-cloud environment\:info -p {st.session_state.projectid} -e {st.session_state.environmentid} | grep -i smtp**")
    st.info(f"**magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \
            \'bin/magento config:show | grep -i mail | grep '@' \'**")
    
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
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid accounts for: **{st.session_state.projectid}**")
        response_sendgrid_accounts = sendgrid_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid)
        if response_sendgrid_accounts:
            st.write(f" ```\n{response_sendgrid_accounts.text.strip()}\n``` ")

with tab2:
    st.header("SendGrid Info")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        
        if st.session_state.env_target_type.lower() != 'containerized':
            apiparameter_value = 1
        else:
            apiparameter_value = 0

        pcresponse = ssh_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            appid=st.session_state.envappid,
                                            apiendpoint='ssh/platformcluster',
                                            apiparameter=apiparameter_value)
        if pcresponse:
            pcresponse_platformcluster = pcresponse.text.strip().replace('"', '')
            print(pcresponse_platformcluster)
            st.write(f" Platform Cluster name Env Var value: ```{pcresponse_platformcluster.strip()}``` ")

            print(response_sendgrid_accounts)
            for indx, sendgridaccountsline in enumerate(response_sendgrid_accounts.text.strip().split('\n')):
                if pcresponse_platformcluster in sendgridaccountsline:
                    if "-master-" in sendgridaccountsline and apiparameter_value == 1:
                        continue
                    sendgridaccountsline = sendgridaccountsline.replace("|", "")
                    print(sendgridaccountsline)
                    st.write(f" ```{sendgridaccountsline}``` ")
                    sendgridaccountlist = sendgridaccountsline.strip().split()
                    print(sendgridaccountlist)
                    print(sendgridaccountlist[0])
                    print("mece-" + pcresponse_platformcluster)
                    if sendgridaccountlist[0] == "mece-" + pcresponse_platformcluster:
                        sendgrid_account_username = sendgridaccountlist[0]
                        break

            st.write(f" Platform SendGrid username for this Env value: ```{sendgrid_account_username.strip()}``` ")
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='info')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("SendGrid Domains")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid domains info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='domains')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("SendGrid Stats")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid stats for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='stats')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("SendGrid Credit")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid credit info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='credit')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("SendGrid Bounce")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid bounce info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='bounce')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("SendGrid Dropped")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid dropped info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='dropped')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("SendGrid Msg Get")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid messages info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='msgget')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab9:
    st.header("SendGrid Msg History")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid messages info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        st.caption(
                f"The History endpoint doesn't have everything (sampling). Sendgrid doesn't offer that under the current Adobe Commerce Cloud subscription.")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='msghist')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab10:
    st.header("SendGrid Blocklist")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting sendgrid blocklist info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if pcresponse:
            response = sendgrid_backend_request(projid=st.session_state.projectid,
                                                envid=sendgrid_account_username.strip(),
                                                apiparameter='blocklist')
            if response:
                st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
