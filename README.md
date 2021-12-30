# Lazy deployment of an attacker infrastructure for log4j RCE CVE-2021-44228

With lord4j, you can quickly deploy a **fully working infrastructure (HTTP & LDAP server) to exploit log4j RCE**.
It is completely **automatic**, run the script with the required args, and let lord4j give you the JNDI string when finished.

<img width="899" alt="Capture d’écran 2021-12-30 à 19 36 51" src="https://user-images.githubusercontent.com/42848077/147779289-04416076-0e63-42bc-b640-309a3301598f.png">

The script relies on threading to be very fast to use.
You will have any return from HTTP/LDAP Server in real time.

## Compatibility

At the moment, lord4j works on **Ubuntu (and apt variants) only**.
You can port it to other platforms (Other Linux or MacOs) by changing the package manager in the code.

You can exploit both **Linux and Windows** and can **run basically any commands you want (one-liner Powershell remote shell for example)**.

## How to install

First, you need to use **Python 3.8 at least**.
Then, install all the required Python modules to be ready to go :

    python3 -m pip install -r requirements.txt
    
## How to use

Lord4j is very lazy, it has only 2 required args and 1 optional.
Better run with **sudo first time**. Lord4j need to install some apt packages.

The first use can be long because it has to build the LDAP Server (It takes aprox. 2m30)

### Local use

If you need to test this in **local** environment :

    sudo python3 lord4j.py -i "your ip" -c "command to be executed on host"

 
### Remote use

If you want to use this on **WAN** environment: (Be sure to open port 8000 and 1389 on your router pointing to the Linux which runs lord4j.)

    sudo python3 lord4j.py -i "your local ip" -c "command to be executed on host" -rip "your remote router ip"


# Credits and stuff

Thanks a lot to mbechter, the entire LDAP Server relies on him : https://github.com/mbechler/marshalsec
Check out this very nice video from John Hammond that helped me understand how this exploit works : https://youtu.be/7qoPDq41xhQ

I'm not responsible of any actions made with this tool. 

You can use it on any application vulnerable to log4j RCE, Minecraft included (that's how i tested it)
