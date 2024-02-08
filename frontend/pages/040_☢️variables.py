import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def variables_backend_request(projid, apiendpoint='variables', envid=None, apioption=None):
    if envid is None:
        envid = 'master'
    if apiendpoint == 'variables' and apioption is None:
        apioption = 'p'
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apioption}")
    #print(resp.text)
    print(resp)
    return resp

@st.cache_data(ttl=1)
def apps_backend_request(projid, envid, apiendpoint='apps', formatvalue='plain', columnsvalue='name', headervalue=0):
    resp = requests.get(
        f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}?format={formatvalue}&columns={columnsvalue}&header={headervalue}")
    #print(resp.text)
    print(resp)
    return resp

st.header("MagCloudy :blue[Environment Variables] :radioactive_sign:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
    st.info(f"**magento-cloud var -p {st.session_state.projectid} -e {st.session_state.environmentid}**")
    st.info(f"**magento-cloud vget -p {st.session_state.projectid} -e {st.session_state.environmentid} ADMIN_FIRSTNAME**")

    st.info(f"**magento-cloud environment\:relationships -p {st.session_state.projectid} -e {st.session_state.environmentid} --no-interaction --property database.0**")
    st.info(f"**magento-cloud environment\:relationships -p {st.session_state.projectid} -e {st.session_state.environmentid} --no-interaction --property redis.0**")

tab1, tab2, tab3 = st.tabs(
    ["Project Vars", "Environment Vars", "Env Relationships"])

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
    response_apps = apps_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid)
    print(response_apps.text)

with tab1:
    st.header("Env Variables at Project Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(f"Getting Env Vars for:  **{st.session_state.projectid}**")
        response = variables_backend_request(projid=st.session_state.projectid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Env Variables at Environment Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Env Vars for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = variables_backend_request(
            projid=st.session_state.projectid, envid=st.session_state.environmentid, apioption='e')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Env Relationships at Environment Level :exclamation:")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting Env Relationships values for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        if response_apps:
            if len(response_apps.text.strip().split()) == 1:
                reqresponse = variables_backend_request(apiendpoint='environments', projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apioption='relationships')
                print(reqresponse)
                st.write(f" ```\n{reqresponse.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response_apps.text.strip().split()):
                    reqresponse = variables_backend_request(apiendpoint='environments', projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid, apioption='relationships')
                    print(indx, inst, reqresponse)
                    st.write(f" ```\n{reqresponse.text.strip()}\n``` ")   

theend()
