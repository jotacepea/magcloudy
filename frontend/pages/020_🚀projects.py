import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import requests

from pages.common.globalconf import pageconfig, theend

pageconfig()

@st.cache_data(ttl=240)
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

st.header("MagCloudy :blue[Projects] :rocket:")

st.header("My Projects")
st.info("**magento-cloud project:list**")

response = projects_backend_request()
print(response)
st.write(f" ```\n{response.text.strip()}\n``` ")

# Project ID Input
main_project_id_input = st.text_input(
    "Enter project id you want to work with: 👇",
    value=st.session_state.projectid if st.session_state.projectid != 'noprojid' else '',
    max_chars=13,
    placeholder="6fck2obu3244c",
)
if main_project_id_input:
    st.session_state.projectid = main_project_id_input

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

# Global ThreadPool Executor in Session State
if 'tp_executor' not in st.session_state:
    st.session_state.tp_executor = ThreadPoolExecutor(max_workers=3)
    st.session_state.environments_cached = None
    st.session_state.environments_cached_full = None

def run_in_thread(func):
    """Decorator to run a function in a separate thread with Streamlit context."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = get_script_run_ctx()

        def func_with_ctx():
            add_script_run_ctx(None, ctx)
            return func(*args, **kwargs)
        return st.session_state.tp_executor.submit(func_with_ctx)
    return wrapper

@run_in_thread
def fetch_tp_envs_pipe(projid, reqfqdn):
    print(f"ENVS PIPE Background fetcher for all project-related metadata for {projid}.")
    try:
        # Environments (Pipe)
        resp = requests.get(f"{reqfqdn}/environments/{projid}/pipe")
        if resp.status_code == 200:
            st.session_state.environments_cached = resp.text.strip().split('\n')
    except Exception as e:
        print(f"Error in background metadata fetch: {e}")

@run_in_thread
def fetch_tp_envs_full(projid, reqfqdn):
    print(f"ENVS FULL Background fetcher for all project-related metadata for {projid}.")
    try:
        # Environments (Full)
        resp = requests.get(f"{reqfqdn}/environments/{projid}")
        if resp.status_code == 200:
            st.session_state.environments_cached_full = resp.text.strip()
    except Exception as e:
        print(f"Error in background metadata fetch: {e}")

if st.session_state.projectid != 'noprojid' and not st.session_state.environments_cached:
    fetch_tp_envs_pipe(
        st.session_state.projectid,
        st.session_state.reqfqdn
    )
    fetch_tp_envs_full(
        st.session_state.projectid,
        st.session_state.reqfqdn
    )

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
        st.info(f"**magento-cloud project:info -p {st.session_state.projectid}**")
        response = projects_backend_request(
            apiendpoint='projects',
            projid=st.session_state.projectid,
            apiparameter='info'
        )
        print(response)
        for indx, projinfoline in enumerate(response.text.strip().split('\n')):
            if 'title' in projinfoline:
                projinfoline = projinfoline.replace("|", "")
                print(projinfoline)
                st.write(f" ```{projinfoline}``` ")
            if 'region' in projinfoline:
                projinfoline = projinfoline.replace("|", "")
                print(projinfoline)
                st.write(f" ```{projinfoline}``` ")
                projregionline = projinfoline.strip().split()
                print(projregionline)
                st.session_state.projectregiondomain = projregionline[1]
        with st.expander("Show Project Info"):
            st.code(response.text.strip(), language='vim')
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
            if 'project_region_label' in projsubsline:
                projsubsline = projsubsline.replace("|", "")
                print(projsubsline)
                st.write(f" ```{projsubsline}``` ")
            if 'plan ' in projsubsline:
                projsubsline = projsubsline.replace("|", "")
                print(projsubsline)
                st.write(f" ```{projsubsline}``` ")
        with st.expander("Show Project Subscription"):
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
        for indx, projsettline in enumerate(response.text.strip().split('\n')):
            if 'development_' in projsettline:
                projsettline = projsettline.replace(",", "")
                print(projsettline)
                st.write(f" ```{projsettline}``` ")
        with st.expander("Show Project Settings"):
            st.code(response.text.strip(), language='json')
with tab4:
    st.header("Users")
    if st.session_state.projectid != 'noprojid':
        st.write("Getting users for Project ID: ",
                 st.session_state.projectid)
        st.info(f"**magento-cloud users -p {st.session_state.projectid}**")
        response = projects_backend_request(
            apiendpoint='users',
            apiparameter=st.session_state.projectid
        )
        print(response)
        with st.expander("Show Project Users"):
            st.code(response.text.strip(), language='vim')

if st.session_state.projectid != 'noprojid':
    theend(enable_select_proj_env_warning = False)
else:
    theend()
