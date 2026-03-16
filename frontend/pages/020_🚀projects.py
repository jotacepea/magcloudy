import streamlit as st
import requests
import json

from pages.common.globalconf import (
    pageconfig,
    run_in_thread,
    clear_cache,
    theend
)

pageconfig()

@st.cache_data(ttl=300, show_spinner="\n\nFetching data from Backend API...")
def projects_backend_request(apiendpoint='projects',projid=None, apiparameter=None):
    if apiparameter is None:
        resp = requests.get(
            f"{st.session_state.reqfqdn}/{apiendpoint}")
    else:
        if projid is None:
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{apiparameter}")
        else:
            resp = requests.get(
                f"{st.session_state.reqfqdn}/{apiendpoint}/{projid}/{apiparameter}")

    print(resp)
    return resp

@run_in_thread
def fetch_tp_my_default_projects():
    print(f"MY DEFAULT PROJECTS Background fetcher for all project-related metadata.")
    try:
        # My Default Projects
        resp = projects_backend_request()
        if resp.status_code == 200:
            st.session_state.my_default_projects = resp.text.strip()
        print(st.session_state.my_default_projects)
    except Exception as e:
        print(f"Error in background metadata fetch: {e}")

@run_in_thread
def fetch_tp_envs_pipe(projid, reqfqdn):
    print(f"ENVS PIPE Background fetcher for all project-related metadata for {projid}.")
    try:
        # Environments (Pipe)
        resp = requests.get(f"{reqfqdn}/environments/{projid}/pipe")
        print(resp.text.strip())
        if resp.status_code == 200:
            st.session_state.environments_pipe_cached = resp.text.strip().split('\n')
    except Exception as e:
        print(f"Error in background metadata fetch: {e}")

@run_in_thread
def fetch_tp_envs_full(projid, reqfqdn):
    print(f"ENVS FULL Background fetcher for all project-related metadata for {projid}.")
    try:
        # Environments (Full)
        resp = requests.get(f"{reqfqdn}/environments/{projid}")
        if resp.status_code == 200:
            st.session_state.environments_full_cached = resp.text.strip()
    except Exception as e:
        print(f"Error in background metadata fetch: {e}")

st.header("MagCloudy :blue[Projects] :rocket:")

st.header("My Projects")
st.info("**magento-cloud project:list**")

fetch_tp_my_default_projects()

col1, col2 = st.columns(2)
with col1:
    # Project ID Input
    main_project_id_input = st.text_input(
        "## Enter Project ID you want to work with:",
        icon=":material/foggy:",
        value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
        max_chars=13,
        placeholder="6fck2obu3244c",
    )
    if main_project_id_input:
        if st.session_state.projectid != main_project_id_input:
            clear_cache()
        st.session_state.projectid = main_project_id_input

    if st.session_state.projectid != 'noprojid' and 'environments_pipe_cached' not in st.session_state:
        fetch_tp_envs_pipe(
            st.session_state.projectid,
            st.session_state.reqfqdn
        )
with col2:
    if st.session_state.projectid != 'noprojid':
        if not st.session_state.get('environments_pipe_cached'):
            print("Fetching environments pipe... Not in session cache!!")
            response_list = projects_backend_request(
                apiendpoint='environments',
                projid=st.session_state.projectid,
                apiparameter='pipe')
            if response_list:
                environments_list = []
                for indx, branchesinfoline in enumerate(response_list.text.strip().split('\n')):
                    print(branchesinfoline)
                    environments_list.append(branchesinfoline)
                print(environments_list)
        else:
            print("Fetching environments pipe... In session cache!!")
            print(st.session_state.environments_pipe_cached)
            environments_list = st.session_state.environments_pipe_cached
    else:
        environments_list=[]

    environment_id_input = st.selectbox(
        "## Choose an environment ID (please, select one of those...) :material/mist:",
        environments_list,
        index=environments_list.index(st.session_state.environmentid) if st.session_state.environmentid != 'noenvid' else None,
        placeholder="Select project ENV...",
    )

    if environment_id_input:
        st.session_state.environmentid = environment_id_input
        if 'environment_info' in st.session_state:
            del st.session_state.environment_info
            
        try:
            # Apps (Pipe)
            resp = requests.get(f"{st.session_state.reqfqdn}/apps/{st.session_state.projectid}/{st.session_state.environmentid}/pipe")
            if resp.status_code == 200:
                st.session_state.envappid = resp.text.strip().split('\n')[0]
        except Exception as e:
            print(f"Error in background apps fetch: {e}")
        
        if 'environments_full_cached' in st.session_state:
            environments_full_cached_debug = json.loads(st.session_state.environments_full_cached)
            for env_values_dict in environments_full_cached_debug:
                print('environment_id_input', environment_id_input)
                print('ID', env_values_dict.get('id'))
                print('deployment_target', env_values_dict.get('deployment_target'))
                
                if env_values_dict.get('id') == environment_id_input:
                    deployment_target = env_values_dict.get('deployment_target')
                    print('deployment_target', deployment_target)
                    break
                else:
                    deployment_target = None
                    print('No match for deployment_target')
            if 'deployment_target' not in st.session_state:
                st.session_state.deployment_target = deployment_target
            elif 'deployment_target' in st.session_state and st.session_state.deployment_target != deployment_target:
                st.session_state.deployment_target = deployment_target

            if 'deployment_target' in st.session_state:
                env_deploy_target = st.session_state.deployment_target
                if env_deploy_target == 'local':
                    st.session_state.env_target_type = 'containerized'
                    st.write(f" **Instances type:** :red[{st.session_state.env_target_type}] ")
                elif env_deploy_target:
                    st.session_state.env_target_type = 'Instances (Unified Cluster)'
                    st.write(f" **Instances type:** :blue[{st.session_state.env_target_type}] ")

# Get Project Web UI/Console URL
if st.session_state.projectid != 'noprojid':
    response = projects_backend_request(
        apiendpoint='webui',
        apiparameter=st.session_state.projectid
    )
    print(response)
    if response:
        st.write(
            f"### Cloud Project [Web UI]({response.text.strip()}) // [ACC Tools](https://acc-tools.corp.adobe.com/project/{st.session_state.projectid}/cluster) ###")

if st.session_state.projectid != 'noprojid' and 'environments_full_cached' not in st.session_state:
    fetch_tp_envs_full(
        st.session_state.projectid,
        st.session_state.reqfqdn
    )

with st.expander("Show your projects list (raw)"):
    if 'my_default_projects' not in st.session_state:
        st.write("No projects found. Please, try again later.")
    else:
        st.write(f" ```\n{st.session_state.my_default_projects}\n``` ")

if st.session_state.projectid != 'noprojid':
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Project Info",
         "Project Subscription",
         "Project Settings",
         "Project Users"])

    with tab1:
        st.header("Info")
        if st.session_state.projectid != 'noprojid':
            st.write("Getting info for Project ID: ",
                     st.session_state.projectid)
            st.info(
                f"**magento-cloud project:info -p {st.session_state.projectid}**"
            )
            response = projects_backend_request(
                apiendpoint='projects',
                projid=st.session_state.projectid,
                apiparameter='info'
            )
            print(response)
            response_json = {}
            try:
                response_json = response.json()
            except Exception:
                pass

        if response_json:
            # Title extraction
            proj_title = response_json.get('title', 'N/A')
            st.write(f" **Title:** `{proj_title}` ")

            # Region extraction
            proj_region = response_json.get('region', 'N/A')
            st.write(f" **Region:** `{proj_region}` ")
            st.session_state.projectregiondomain = proj_region

            # Subscription info
            subscription = response_json.get('subscription', {})
            proj_plan = subscription.get('plan', 'N/A')
            proj_envs = subscription.get('environments', 'N/A')
            proj_storage = subscription.get('storage', 'N/A')

            st.write(f" **Plan:** `{proj_plan}` ")
            st.write(f" **Environments:** `{proj_envs}` ")
            st.write(f" **Storage:** `{proj_storage} MB` ")
        else:
            # Fallback for previous text-based parsing
            for indx, projinfoline in enumerate(response.text.strip().split('\n')):
                if 'title' in projinfoline:
                    projinfoline = projinfoline.replace("|", "").strip()
                    st.write(f" **Title:** `{projinfoline.split('title')[1].strip()}` ")
                if 'plan:' in projinfoline:
                    projinfoline = projinfoline.replace("|", "").strip()
                    st.write(f" **Plan:** `{projinfoline.split('plan:')[1].strip()}` ")
                if 'environments:' in projinfoline:
                    projinfoline = projinfoline.replace("|", "").strip()
                    st.write(
                        f" **Environments:** `{projinfoline.split('environments:')[1].strip()}` "
                    )
                if 'storage:' in projinfoline:
                    projinfoline = projinfoline.replace("|", "").strip()
                    st.write(
                        f" **Storage:** `{projinfoline.split('storage:')[1].strip()}` "
                    )
                if 'region' in projinfoline:
                    projinfoline = projinfoline.replace("|", "").strip()
                    st.write(
                        f" **Region:** `{projinfoline.split('region')[1].strip()}` "
                    )
                    projregionline = projinfoline.split()
                    if len(projregionline) > 1:
                        st.session_state.projectregiondomain = projregionline[1]

        with st.expander("Show Project Info (raw)"):
            st.code(response.text.strip(), language='json')
    with tab2:
        st.header("Subscription")
        if st.session_state.projectid != 'noprojid':
            st.write("Getting Subscription info for Project ID: ",
                     st.session_state.projectid)
            st.info(f"**magento-cloud subscription:info -p {st.session_state.projectid}**")
            response = projects_backend_request(
                apiendpoint='projects',
                projid=st.session_state.projectid,
                apiparameter='subscription'
            )
            print(response)
            for indx, projsubsline in enumerate(response.text.strip().split('\n')):
                if 'username:' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Username:** `{projsubsline.split('username:')[1].strip()}` ")
                if 'project_id ' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Project ID:** `{projsubsline.split('project_id')[1].strip()}` ")
                if 'project_title' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Project Title:** `{projsubsline.split('project_title')[1].strip()}` ")
                if 'InstanceRole:' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Instance Role:** `{projsubsline.split('InstanceRole:')[1].strip()}` ")
                if 'project_region_label' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Region Label:** `{projsubsline.split('project_region_label')[1].strip()}` ")
                if 'plan ' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    st.write(f" **Plan:** `{projsubsline.split('plan')[1].strip()}` ")
                if 'hipaa ' in projsubsline:
                    projsubsline = projsubsline.replace("|", "").strip()
                    hipaa_val = projsubsline.split('hipaa')[1].strip()
                    if hipaa_val == 'true':
                        st.write(f" **HIPAA:** :red[{hipaa_val}] ")
                    else:
                        st.write(f" **HIPAA:** :green[{hipaa_val}] ")
            with st.expander("Show Project Subscription (raw)"):
                st.code(response.text.strip(), language='vim')
    with tab3:
        st.header("Settings")
        if st.session_state.projectid != 'noprojid':
            st.write("Getting settings for Project ID: ",
                     st.session_state.projectid)
            st.info(f"**magento-cloud project:curl -p {st.session_state.projectid} /settings**")
            response = projects_backend_request(
                apiendpoint='projects',
                projid=st.session_state.projectid,
                apiparameter='settings'
            )
            print(response)
            response_json = {}
            try:
                response_json = response.json()
            except Exception:
                pass

            if response_json:
                # Title extraction
                init_title = response_json.get('initialize', {}).get('stack', {}).get('title', 'N/A')
                base_title = response_json.get('initialize', {}).get('values', {}).get('base', {}).get('title', 'N/A')
                st.write(f" **Stack Title:** `{init_title}` ")
                st.write(f" **Base Title:** `{base_title}` ")

                # Product info
                prod_name = response_json.get('product_name', 'N/A')
                prod_code = response_json.get('product_code', 'N/A')
                st.write(f" **Product:** `{prod_name} -- {prod_code}` ")

                # Disk info
                temp_disk = response_json.get('temporary_disk_size', 'N/A')
                local_disk = response_json.get('local_disk_size', 'N/A')
                st.write(f" **Disk:** `Temp: {temp_disk} MB` / `Local: {local_disk} MB` ")

                # Previous development_ service info (preserved if present in keys)
                dev_serv = response_json.get('development_service_size', 'N/A')
                dev_app = response_json.get('development_application_size', 'N/A')
                st.write(f" **Dev Size:** `Service: {dev_serv}` / `App: {dev_app}` ")
            else:
                # Fallback for non-JSON or partial text
                for indx, projsettline in enumerate(response.text.strip().split('\n')):
                    if 'development_' in projsettline:
                        projsettline = projsettline.replace(",", "").replace('"', '').strip()
                    st.write(f" ```{projsettline}``` ")
        
            with st.expander("Show Project Settings (raw)"):
                st.code(response.text.strip(), language='json')
    with tab4:
        st.header("Users")
        if st.session_state.projectid != 'noprojid':
            st.write("Getting users for Project ID: ",
                     st.session_state.projectid)
            st.info(f"**magento-cloud users -p {st.session_state.projectid} -q**")
            response_user_owner = projects_backend_request(
                apiendpoint='users',
                projid=st.session_state.projectid,
                apiparameter='owner'
            )
            print(response_user_owner.text)
            owner_display_name = "N/A"
            if response_user_owner and response_user_owner.text:
                for line in response_user_owner.text.strip().split('\n'):
                    print(line)
                    if ':' in line:
                        k, v = line.split(':', 1)
                        if k.strip() in ['display_name']:
                            owner_display_name = v.strip()
                            break
            st.success(f"Project Owner: **{owner_display_name}**")

            response = projects_backend_request(
                apiendpoint='users',
                apiparameter=st.session_state.projectid
            )
            # Parse JSON list response
            users_data = []
            try:
                response_json = response.json()
                if isinstance(response_json, list):
                    for user_item in response_json:
                        role = user_item.get('role', 'N/A')
                        # Extract user details from _embedded.users[0]
                        embedded_users = user_item.get('_embedded', {}).get('users', [])
                        if embedded_users:
                            user_info = embedded_users[0]
                            display_name = user_info.get('display_name', 'N/A')
                            email = user_info.get('email', 'N/A')

                            if display_name in owner_display_name:
                                role = f"**{role} (Owner)**"
                            
                            users_data.append({
                                "Name": display_name,
                                "Email": email,
                                "Role": role
                            })
            except Exception as e:
                st.error(f"Error parsing user JSON: {e}")

            if users_data:
                st.table(users_data)
            else:
                # Fallback or empty state
                st.warning("No user data found in the response.")

            with st.expander("Show Project Users (raw)"):
                st.code(response.text.strip(), language='json')

if st.session_state.projectid != 'noprojid':
    theend(enable_select_proj_env_warning=False)
else:
    theend()
