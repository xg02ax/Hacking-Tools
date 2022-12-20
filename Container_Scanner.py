###here we beging to work on our workflow(orchestrator)

import json
import subprocess ###to be able to make the call out to the command line for klar

import socket ###low lvl networking interface library to allow the creation of network connections within the script
import argparse ###interprets arguments passed to the script
import sys  ###allows access to system-specific parameters and functions
from datetime import datetime ###gets time within the script


CLAIR_PATH = "/Users/geovanniarroyoLacen/go/bin/clair-scanner"
parser = argparse.ArgumentParser() ###initializes the parse so you can add custom arguments
parser.add_argument('host') ###gets host IP which is needed to be passed to our script
args = parser.parse_args()


def python_ping(host, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(3)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            print ("Host down")
    except socket.gaierror:
            print ("some wrong with the host")


def port_scanner():
    try:

        t1 = datetime.now() ###gets current time
        for port in range(1, 24): ###this creates a for loop that goes through the most common docker ports used to host services
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ###within the loop this creates a socket to try and connect to the IP address provided over the port
            sock.settimeout(1) ###If results equal to 0, the connection is succesfull and script will let us know that the port is open
            result = sock.connect_ex((args.host, port))
            if result == 0: ###If results equal to 0, the connection is succesfull and script will let us know that the port is open
                print("Port: {} Open".format(port))
            sock.close() ###closes the socket and does this process again in the next port
        t2 = datetime.now()
        print("Scanning completed in: {}".format(t2-t1)) ###once the scan has been completed on all ports, this will print out how long the script ran for
    except:
        return False


def image_scanner(): ### fuction to run clair in the command line once the script has been called
    try:
            result = subprocess.run(["{}".format(CLAIR_PATH), "--report=""/Users/geovanniarroyolacen/TOOLS/TOOLS_code/temp.json""", "--ip", "192.168.1.5", "vulnerables/web-dvwa"], capture_output=True, text=True) ##here you need to put the absolute path to your clair-scanner dir, your local IP and the image being scanned
            print(result.stdout)
            print(result.stderr)
    except FileNotFoundError:
        print('Clair path not found, {}'.format(CLAIR_PATH))        


def main():
    python_ping(args.host, 80)
    port_scanner()   
    #image_scanner()


if __name__ == "__main__": 
    main()