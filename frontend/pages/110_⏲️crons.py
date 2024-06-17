import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

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

st.header("MagCloudy :blue[Crons] :timer_clock:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info("**php bin/magento config\:show | grep -i cron**")
    st.info("**php bin/magento cron -h**")
    st.info("**php vendor/bin/ece-tools cron -h**")
    st.info(f"""
       **magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} \
            \"find ./app/ ./vendor/ -name 'cron_groups.xml' | xargs grep 'group id' | awk '{{print \\\$3}}' | sort | \
                uniq | sed 's/id=//g' | sed 's/>//g' | xargs -I {{}} echo --group={{}}  \"**
        """)
    
tab1, tab2, tab3 = st.tabs(
    ["CronTab",
     "Cron List",
     "Cron Status"])

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    response_instances = ssh_backend_request(projid=st.session_state.projectid,
                                             envid=st.session_state.environmentid,
                                             appid=st.session_state.envappid)
    print(response_instances)

with tab1:
    st.header("Crontab")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Reading CronTab Info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        if response_instances:
            if len(response_instances.text.strip().split()) == 1:
                st.caption(
                    "**Note:** :bricks: for containerized environments... crontab could be NOT allowed!!!)")
                st.write(
                    f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} 'crontab -l'``` ")
                reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                  envid=st.session_state.environmentid,
                                                  appid=st.session_state.envappid,
                                                  apiendpoint='ssh/crontab',
                                                  apiparameter=0)
                print(reqresponse)
                st.write(f" ```\n{reqresponse.text.strip()}\n``` ")
            else:
                for indx, inst in enumerate(response_instances.text.strip().split()):
                    st.write(
                        f" ``` magento-cloud ssh -p {st.session_state.projectid} -e {st.session_state.environmentid} -I {indx + 1} 'crontab -l'``` ")
                    reqresponse = ssh_backend_request(projid=st.session_state.projectid,
                                                      envid=st.session_state.environmentid,
                                                      appid=st.session_state.envappid,
                                                      apiendpoint='ssh/crontab',
                                                      apiparameter=indx + 1)
                    print(indx, inst, reqresponse)
                    st.write(f" ```\n{reqresponse.text.strip()}\n``` ")

with tab2:
    st.header("Cron List")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Crons for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/cronlist")
        print(response)
        if response:
            code_query_line="select job_code, created_at from cron_schedule group by job_code;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Cron Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Getting Crons for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/othercron")
        print(response)
        if response:
            code_query_line1="select count(*), status, job_code, created_at, scheduled_at, executed_at, finished_at, messages from cron_schedule where job_code NOT like 'consumers%' and job_code NOT like 'indexer%' and DATE(created_at) = DATE(CURDATE()) group by status, job_code;"
            st.code(code_query_line1, language='bash')
            code_query_line2="select count(*) as ccc, job_code, created_at, scheduled_at, executed_at, status FROM cron_schedule WHERE status != 'error' GROUP BY job_code, status HAVING ccc > 1 ORDER BY job_code, status;"
            st.code(code_query_line2, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
