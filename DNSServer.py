import socket 
import os
import json 
import sys
import utils
import threading 
import logging
import utils
import time
from getmac import get_mac_address as gma 

HOST_CONF_FILE = '/etc/dnsmasq.d/hosts.conf'
DNS_RQ_PORT = 23333



logging.basicConfig(datefmt='%d-%b-%y %H:%M:%S',
    format='[%(asctime)s] %(levelname)s DNS_Service: %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger('DNS Service')

class DNSServer(object):
    def __init__(self):  
        self.__provision()
        dealers = {
            'register': self.__registerNode,
        }
        tRecv = threading.Thread(target=utils.recv,\
            args=(("0.0.0.0", DNS_RQ_PORT), dealers, logger))
        tRecv.start()


    def __provision(self):
        logger.info("start provisioning")
        if not os.geteuid() == 0:
            logger.error("This script must be"\
                + "executed under super user")
            sys.exit(1)
        os.system('fuser -k 53/udp')
        os.system("echo '' > %s"%HOST_CONF_FILE)
        os.system('fuser -k 53/tcp')
        os.system('fuser -k 23333/tcp')
        os.system('fuser -k 23333/udp')
        os.system('systemctl start dnsmasq')


    def __registerNode(self, params):
        member = {
            'ip': params['ip'],
            'domainName':params['domainname']
        }
        if not len(
            os.popen('cat %s | grep %s'%(HOST_CONF_FILE, params['domainname'])).read()
        ) == 0:
            return False

        record = 'address=/%s/%s\n'%(params['domainname'], params['ip'])
        with open(HOST_CONF_FILE, 'a+') as dnsConfFile:
            dnsConfFile.write(record)
        os.system('systemctl restart dnsmasq')
        regisResult = {
            'result': True
        }
        logger.info(str(regisResult))
        return regisResult
            
if __name__ == "__main__":
    dnsserver = DNSServer()
    
    
    # 82693332
