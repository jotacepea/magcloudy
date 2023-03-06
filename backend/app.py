from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import subprocess
import os

# print(os.environ['MAGENTO_CLOUD_CLI_TOKEN'])

app = Flask(__name__)
CORS(app)


ip_whitelist = ['192.168.1.2', '192.168.1.3']


def valid_ip():
    client = request.remote_addr
    if client in ip_whitelist:
        return True
    else:
        # Check source IP, right now disabled!!!
        # return False
        return True


@app.route('/')
def index():
    return "Hi from MagCloudy API!!"


pong = [
    {'description': 'healthcheck', 'status': "pong"}
]


@app.route('/ping')
def health():
    return jsonify(pong)


@app.route('/check')
@cross_origin(origin='*')
def get_check():
    if valid_ip():
        command_version = "magento-cloud -V"
        command_check = "magento-cloud auth:info"
        # command_check = "env|grep MAGE"
        try:
            result_command_version = subprocess.check_output(
                [command_version], shell=True, env=os.environ, universal_newlines=True).split('\n')
            result_command_check = subprocess.check_output(
                [command_check], shell=True, env=os.environ, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to shell cmd: %s" % e
        return 'Version --> %s \n\nCheck -->  %s' % (result_command_version, result_command_check)
    else:
        return """<title>404 Not Found</title>
               <h1>Not Found</h1>
               <p>The requested URL was not found on the server.
               If you entered the URL manually please check your
               spelling and try again.</p>""", 404


@app.route('/magecloud')
def run_magecloud():
    if valid_ip():
        req_paramsparam = request.args.get('cmdparam', "list")
        command_magecloud = f"magento-cloud {req_paramsparam}"
        try:
            result_command_magecloud = subprocess.check_output(
                [command_magecloud], shell=True, env=dict(os.environ), universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to shell cmd: %s" % e

        return f"Output:\n\n{result_command_magecloud}"
    else:
        return """<title>404 Not Found</title>
               <h1>Not Found</h1>
               <p>The requested URL was not found on the server.
               If you entered the URL manually please check your
               spelling and try again.</p>""", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
