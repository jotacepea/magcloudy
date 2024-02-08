import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=300)
def newrelic_backend_request(projid, envid, apiendpoint='newrelic', apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{envid}/{projid}")
    else:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{envid}/{apiparameter}")
    print(resp)
    return resp

st.header("MagCloudy :blue[NewRelic] :chart_with_upwards_trend:")

st.caption(
    f"[NewRelic GraphQL API Explorer](https://one.newrelic.com/nerdgraph-graphiql) // \
    [NewRelic Cli](https://github.com/newrelic/newrelic-cli)")

tab1, tab2, tab3 = st.tabs(
    ["NewRelic Actor",
     "NewRelic Account",
     "NewRelic Transactions"])

with tab1:
    st.header("NewRelic Actor")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid accounts for: **{st.session_state.projectid}**")
        response = newrelic_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("NewRelic Account")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting sendgrid accounts for: **{st.session_state.projectid}**")
        response = newrelic_backend_request(projid=st.session_state.projectid,
                                            envid=st.session_state.environmentid,
                                            apiparameter='account')
        if response:
            for indx, nrinfoline in enumerate(response.text.strip().split('\n')):
                if '"id":' in nrinfoline:
                    nrinfoline = nrinfoline.replace(",", "")
                    nr_account_id=nrinfoline.strip().split(':')[1]
                    print(nrinfoline)
                    print(nr_account_id)
                    #st.write(f" ```{nrinfoline}``` ")
                    #st.write(f" ```{nr_account_id}``` ")
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("NewRelic Transactions")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting newrelic app transactions for: **{st.session_state.projectid}**")
        response = newrelic_backend_request(projid=st.session_state.projectid,
                                            envid=nr_account_id,
                                            apiparameter='transactions')
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")


theend()
