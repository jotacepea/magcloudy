import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[DB] :thread:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info(f"**magento-cloud sql -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r database**")
    if st.session_state.env_target_type.lower() != 'containerized':
        st.info(f"**magento-cloud sql -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r database-slave**")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    ["Db Version",
     "Db Size",
     "Db Tables Size",
     "Db Process",
     "DB Status",
     "Cluster Status",
     "MyISAM tables",
     "Primary Key on tables",
     "Percona Tool MySQL Summary"])

with tab1:
    st.header("DB Version")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Reading DB version for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/version")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab2:
    st.header("DB Size")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB size for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        st.caption(
            "**Note:** this section works for containerized environments only :bricks:)")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/size")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab3:
    st.header("DB Table Size")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB Tables size for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/tablesize")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("DB Process")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB process list for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/processw")
        print(response)
        if response:
            st.write("Write connection...")
            st.write(f" ```\n{response.text.strip()}\n``` ")
        if st.session_state.env_target_type.lower() != 'containerized':
            response = requests.get(
                f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/processr")
            print(response)
            if response:
                st.write("Read connection...")
                st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
    st.header("DB Stats")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting DB cluster status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/status")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        st.write(f"No DB status info --> {st.session_state.env_target_type}")

with tab6:
    st.header("DB Cluster Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting DB cluster status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/wsrep")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        st.write(f"No DB Cluster info --> {st.session_state.env_target_type}")

with tab7:
    st.header("Check MyISAM tables")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting DB tables status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/myisam")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        st.write(f"No DB tables info --> {st.session_state.env_target_type}")

with tab8:
    st.header("Check Primary KEY on tables")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting DB tables status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/primarykey")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        st.write(f"No DB tables info --> {st.session_state.env_target_type}")


with tab9:
    st.header("PT MySQL Summary")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting PT Summary for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/ssh/ptmysqlsummary/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/1")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")
    else:
        response = requests.get(
            f"{st.session_state.reqfqdn}/ssh/ptmysqlsummary/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}")
        print(response)
        if response:
            st.write(f" ```\n{response.text.strip()}\n``` ")

theend()
