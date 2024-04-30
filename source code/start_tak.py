import subprocess
import os

status = {
    'message': '',
    'ip': ''
}

def start_tak():
    tak_enable = 'sudo systemctl enable takserver.service'
    tak_start = 'sudo systemctl start takserver.service'
    tak_status = 'service --status-all | grep "takserver"'
    ip_check = 'ip addr show | grep -oE "inet (addr:)?([0-9]*\.){3}[0-9]*"'


    if('tak' in os.listdir('/opt')):
        if('files' not in os.listdir('/opt/tak/certs')):
            status['message'] = 'TAK admin cert needs to be generated to start TAK server.'
        else:
            current_tak_status = subprocess.run(tak_status, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')
            if(' [ - ]  takserver' in current_tak_status):
                status['message'] = 'TAK server needs to be started.'
            else:
                status['ip'] = 'TAK server running on https://' + subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[1] + ':8443'
                subprocess.run(tak_enable.split(' '))
                subprocess.run(tak_start.split(' '))
    else:
        print(subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[1].split(' ')[1])
        status['message'] = 'TAK server needs to be installed.'