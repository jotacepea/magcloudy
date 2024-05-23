import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[Queues] :factory:")

tab1, tab2, tab3, tab4 = st.tabs(
    ["DB Queues",
     "DB Queue Messages",
     "DB Queues Status",
     "DB Queues Trials"])

with tab1:
    st.header("Queues")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
        st.write(
            f"Reading db queues for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/queuelist")
        print(response)
        if response:
            code_query_line="select id, name from queue;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("Messages")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting messages info for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/queuemessages")
        print(response)
        if response:
            code_query_line="select count(*) as Messages, topic_name from queue_message group by topic_name;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting message status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/queuemsgstatus")
        print(response)
        if response:
            code_query_line="select count(*), topic_name, queue_id, updated_at, status from queue_message qm inner join queue_message_status qms on qm.id = qms.message_id where DATE(updated_at) > DATE(CURDATE()-5) group by topic_name, status limit 50;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("Trials")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting message status trials for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/queuemsgtrials")
        print(response)
        if response:
            code_query_line="select count(*), name, status, number_of_trials from queue_message_status s join queue q on s.queue_id = q.id where DATE(updated_at) > DATE(CURDATE()-5) group by status, name, number_of_trials limit 50;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")
        
theend()
