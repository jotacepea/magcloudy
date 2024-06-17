# How to review and debug Adobe Commerce Cloud project environments: MagCloudy

Work in progress...

## Why MagCloudy?

MagCloudy is a local tool running in docker containers for reviewing and for debugging Adobe Commerce Cloud enviroments when something is wrong there.

## Requirements

- Docker and Docker Compose: [Install](https://docs.docker.com/guides/getting-started/get-docker-desktop/#explanation)
- Magento Cloud CLI: [API Token](https://experienceleague.adobe.com/en/docs/commerce-cloud-service/user-guide/project/multi-factor-authentication#connect-to-an-environment-using-ssh-with-an-api-token)

## Good to have

- Magento Cloud CLI: [Install](https://experienceleague.adobe.com/en/docs/commerce-cloud-service/user-guide/dev-tools/cloud-cli/cloud-cli-overview)
- Python Cluster Shell: [Clush](https://clustershell.readthedocs.io/en/latest/install.html#installing-clustershell-as-user-using-pip)
- NewRelic: [User API Key](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/)

## Run the app

Use `docker-compose.yml`

Export New Relic User API Key (Not mandatory, WiP):
```console
export NEW_RELIC_API_KEY='KARN-ZMK***WRQ***4P4***QJ9***KOK'
```

Export Magento Cloud CLI API Key:
```console
export MAGENTO_CLOUD_CLI_TOKEN='036***b710***1491***f03fg***6f09bc***e45'
```

```console
docker compose up --build
docker compose down
```

MagCloudy app in your browser:
http://localhost:8888


## MagCloudy local tool components

BackEnd container ofering API (python) running commands: Magento Cloud CLI, SSH, NewRelic CLI and Flastly CLI (some of them in WiP).

FrontEnd container offering GUI in Python [Streamlit](https://docs.streamlit.io/get-started/installation/command-line#install-streamlit-in-your-environment)

## Why Streamlit?

Because it is very easy to create web pages and you do not need to have deep knowledge about HTML, CSS and JS.
Of course, if you have this frontend knowledge then, you can create even better web pages.

Streamlit scripts are executed secuentially then, we do not put extra work over the environemnt we are reviewing.

More [info](https://docs.streamlit.io/get-started/fundamentals/summary).

## Notes

- The Adobe Global Protect VPN can add some small delay to the background commands.
- Sometimes and for some projects, the Magento Cloud API service has performance issues.


