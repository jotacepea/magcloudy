import streamlit as st
import requests
from pages.common.globalconf import pageconfig, theend

pageconfig()

st.header("MagCloudy :blue[DB] :thread:")

if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.envappid != 'noenvappid':
    st.info(f"**magento-cloud sql -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r database**")
    if st.session_state.env_target_type.lower() != 'containerized':
        st.info(f"**magento-cloud sql -p {st.session_state.projectid} -e {st.session_state.environmentid} -A {st.session_state.envappid} -r database-slave**")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    ["Db Version",
     "Db Size",
     "Db Tables Size",
     "Db Tables Frag Ratio",
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
            code_query_line="SELECT table_schema as `Database`, table_name AS `Table`, ROUND(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` FROM information_schema.TABLES ORDER BY (data_length + index_length) DESC LIMIT 15;"
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab4:
    st.header("DB Table Frag Space")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid':
        st.write(
            f"Getting DB Tables Frag Free size for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/tablesizefragratio")
        print(response)
        if response:
            code_query_line="""SELECT ENGINE, TABLE_SCHEMA AS `Db`, TABLE_NAME AS `Table`, 
                ROUND(((DATA_LENGTH) / 1024 / 1024), 2) as `Size in MB`, ROUND(((INDEX_LENGTH) / 1024 / 1024), 2) as `Index in MB`, ROUND(DATA_FREE/1024/1024, 2) as `Free in MB`, 
                (DATA_FREE/(INDEX_LENGTH+DATA_LENGTH)) as frag_ratio 
                FROM information_schema.TABLES 
                WHERE DATA_FREE > 0 
                ORDER BY DATA_FREE DESC LIMIT 15;
                """
            st.code(code_query_line, language='bash')
            st.write(f" ```\n{response.text.strip()}\n``` ")

with tab5:
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

with tab6:
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

with tab7:
    st.header("DB Cluster Status")
    if st.session_state.projectid != 'noprojid' and st.session_state.environmentid != 'noenvid' and st.session_state.env_target_type.lower() != 'containerized':
        st.write(
            f"Getting DB cluster status for: **{st.session_state.envappid}** in **{st.session_state.environmentid}** from **{st.session_state.projectid}**")
        response = requests.get(
            f"{st.session_state.reqfqdn}/db/{st.session_state.projectid}/{st.session_state.environmentid}/{st.session_state.envappid}/wsrep")
        print(response)
        if response:
            wsrep_data = response.text.strip()

            # Highlighting wsrep_local_recv_queue related metrics
            try:
                # Basic parsing of the table output
                lines = wsrep_data.split('\n')
                recv_wsrep_queue_values = {}
                for line in lines:
                    if '|' in line and 'wsrep_local_recv_queue' in line:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 3:
                            key = parts[1]
                            val = parts[2]
                            recv_wsrep_queue_values[key] = val

                if recv_wsrep_queue_values:
                    st.subheader("Receive Queue Metrics Highlight :chart_with_upwards_trend:")
                    
                    # Convert values to float for checking
                    try:
                        current_queue = float(recv_wsrep_queue_values.get('wsrep_local_recv_queue', 0))
                    except (ValueError, TypeError):
                        current_queue = 0
                    
                    # Display metrics in a nice ST Format
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("WSREP Current Queue", recv_wsrep_queue_values.get('wsrep_local_recv_queue', 'N/A'), 
                               delta=None, delta_color="inverse")
                    col2.metric("WSREP Max Queue", recv_wsrep_queue_values.get('wsrep_local_recv_queue_max', 'N/A'))
                    col3.metric("WSREP Min Queue", recv_wsrep_queue_values.get('wsrep_local_recv_queue_min', 'N/A'))
                    col4.metric("WSREP Avg Queue", recv_wsrep_queue_values.get('wsrep_local_recv_queue_avg', 'N/A'))

                    if current_queue > 0:
                        st.error(f"⚠️ **Warning:** `wsrep_local_recv_queue` is **{current_queue}**!")
                        st.error("This indicates that the DB node cannot keep up with the replication rate.")
                    else:
                        st.success("✅ `wsrep_local_recv_queue` is 0.")
                        st.success("DB Nodes are keeping up with replication.")

                # Highlighting wsrep_cluster_size and wsrep_cluster_weight
                cluster_metrics = {}
                for line in lines:
                    if '|' in line and ('wsrep_cluster_size' in line or 'wsrep_cluster_weight' in line):
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 3:
                            cluster_metrics[parts[1]] = parts[2]

                if cluster_metrics:
                    st.subheader("Cluster Topology Metrics Highlight :dolls:")
                    col1, col2 = st.columns(2)
                    
                    size_val = cluster_metrics.get('wsrep_cluster_size', 'N/A')
                    weight_val = cluster_metrics.get('wsrep_cluster_weight', 'N/A')
                    
                    col1.metric("WSREP Cluster Size", size_val)
                    col2.metric("WSREP Cluster Weight", weight_val)

                    try:
                        size_int = int(size_val)
                    except (ValueError, TypeError):
                        size_int = 0

                    try:
                        weight_int = int(weight_val)
                    except (ValueError, TypeError):
                        weight_int = 0

                    if size_int != 3:
                        st.error(f"⚠️ **Warning:** `wsrep_cluster_size` is **{size_val}**! Expected value is 3.")
                    else:
                        st.success(f"✅ `wsrep_cluster_size` is **{size_val}**.")

                    if weight_int != 3:
                        st.error(f"⚠️ **Warning:** `wsrep_cluster_weight` is **{weight_val}**! Expected value is 3.")
                    else:
                        st.success(f"✅ `wsrep_cluster_weight` is **{weight_val}**.")

            except Exception as e:
                st.error(f"Error parsing wsrep values: {e}")
            
            with st.expander("Show Raw Galera Status Output"):
                st.write(f" ```\n{wsrep_data}\n``` ")
    else:
        st.write(f"No DB Cluster info --> {st.session_state.env_target_type}")

with tab8:
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

with tab9:
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


with tab10:
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
        st.write(f"No DB Percona Tool info --> {st.session_state.env_target_type}")

theend()
