import os
import json
import socket
import utils
import time



with open('name.conf', 'r') as f:
    domainname = f.read()
conn = ('47.103.45.126', 23333)
current_ip = ""
while True:
    if not current_ip == utils.getIP():
        current_ip = utils.getIP()
        print(utils.send(conn, json.dumps({
            'type': 'register',
            'params': {
                'ip': utils.getIP(),
                'domainname': domainname
            }
        })))
    time.sleep(60)
    
