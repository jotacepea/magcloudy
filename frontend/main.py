import os
import streamlit as st
from pages.common.globalconf import pageconfig, set_default_cache_values, theend

st.session_state.default_api_backend_name = os.environ.get("DEFAULT_API_BACKEND_NAME", "apibackend")
st.session_state.default_api_backend_port = os.environ.get("DEFAULT_API_BACKEND_PORT", "5000")
st.session_state.reqfqdn = f"http://{st.session_state.default_api_backend_name}:{st.session_state.default_api_backend_port}"

pageconfig()

st.warning('This is a MagCloudy Beta Version!!!', icon="⚠️")

###st.snow()

st.write("# Welcome to MagCloudy! :dizzy:")

st.sidebar.success("Select an option above.")

st.markdown(
    """
    MagCloudy is a tool built specifically for
    interacting with Adobe Commerce Cloud projects.

    ### Want to learn more?
    - Check out [cloud-cli](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/dev-tools/cloud-cli.html?lang=en)
    - Jump into our [documentation](https://experienceleague.adobe.com/docs/commerce-cloud-service/user-guide/overview.html?lang=en)
    
    ### Cloud Projects:
    - Magento Cloud [projects](https://accounts.magento.cloud/admin/platform/projects)
    - Magento Cloud [regions](https://accounts.magento.cloud/admin/commerce/platform/regions)

"""
)

set_default_cache_values()

theend(enable_select_proj_env_warning = False)