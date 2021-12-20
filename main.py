import subprocess
import os

maven = subprocess.Popen('sudo apt install maven', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
print('Installing maven..')
maven.wait()

tttt
