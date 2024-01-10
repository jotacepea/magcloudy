import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()


@st.cache_data(ttl=300)
def fastly_backend_request(projid, envid, apiendpoint='fastly', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp


st.header("MagCloudy :blue[Fastly] :shield:")

st.caption(
    f"[Fastly GUI](https://manage.fastly.com/) // \
    [Fastly Cli](https://developer.fastly.com/reference/cli/)")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(
    ["Fastly Module",
     "Fastly Credentials",
     "Fastly Service",
     "Fastly Backends",
     "Fastly Domains",
     "Fastly Stats",
     "Fastly VLC Objects",
     "Fastly ACLs",
     "Fastly Products",
     "Fastly TLS Configurations",
     "Fastly Rate Limit",
     "Fastly Healthchecks"])

with tab1:
    st.header("Fastly Module")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly module status for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Fastly Credentials")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly credentials for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            apiparameter='credentials')
        if response:
            print(response)
            for indx, fastcredline in enumerate(response.text.strip().split('\n')):
                if f'{st.session_state.projectid}' in fastcredline:
                    fastsrvline = fastcredline.split(':')
                    print(fastsrvline)
                    print(fastsrvline[1])
                    fast_srv_name=fastsrvline[1]
                    st.write(f" ```{fast_srv_name}``` ")
                if ' ID:' in fastcredline:
                    fastidline = fastcredline.split(':')
                    print(fastidline)
                    print(fastidline[1])
                    fast_srv_id=fastidline[1]
                    st.write(f" ```{fast_srv_id}``` ")
                if ' Token:' in fastcredline:
                    fasttokline = fastcredline.split(':')
                    print(fasttokline)
                    print(fasttokline[1])
                    fast_token=fasttokline[1]
                    st.write(f" ```{fast_token}``` ")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Fastly Service")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly service info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'service?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Fastly Backends")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly backends info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'backend?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("Fastly Domains")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly domains info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'domain?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab6:
    st.header("Fastly Stats")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly stats info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'stats?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab7:
    st.header("Fastly VCL Objects")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly vcl info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'vclcondition?fast_token={fast_token}')
        if response:
            st.write("**conditions**")
            st.write(f" ```\n{response.text.strip()}\n``` ")

        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'vclcustom?fast_token={fast_token}')
        if response:
            st.write("**custom**")
            st.write(f" ```\n{response.text.strip()}\n``` ")

        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'vclsnippet?fast_token={fast_token}')
        if response:
            st.write("**snippets**")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab8:
    st.header("Fastly ACLs")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly acls info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'acl?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab9:
    st.header("Fastly Products")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly products info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'products?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab10:
    st.header("Fastly TLS Configurations")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly products info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'tlsconfig?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab11:
    st.header("Fastly Rate Limit")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly rate limit info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'ratelimit?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab12:
    st.header("Fastly Healthchecks")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting fastly healthchecks info for: **{st.session_state.projectid}** in **{st.session_state.environmentid}**")
        response = fastly_backend_request(projid=fast_srv_name,
                                            envid=fast_srv_id,
                                            apiparameter=f'healthcheck?fast_token={fast_token}')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
