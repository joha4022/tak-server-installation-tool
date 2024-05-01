import subprocess
import os

status = {
    'message': '',
    'ip': '',
    'start_button_state': '',
    'stop_button_state': ''
}

def start_tak():
    tak_enable = 'sudo systemctl enable takserver.service'
    tak_start = 'sudo systemctl start takserver.service'
    tak_status = 'service --status-all | grep "takserver"'
    ip_check = 'ip addr show | grep -oE "inet (addr:)?([0-9]*\.){3}[0-9]*"'

    if('tak' in os.listdir('/opt')):
        if('files' not in os.listdir('/opt/tak/certs')):
            status['message'] = 'Generate Root / Server / Admin certificates'
            status['start_button_state'] = 'disabled'
            status['stop_button_state'] = 'disabled'
        else:
            current_tak_status = subprocess.run(tak_status, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')
            if(' [ - ]  takserver' in current_tak_status):
                status['message'] = 'TAK server not running'
                status['start_button_state'] = 'active'
                status['stop_button_state'] = 'disabled'
            else:
                status['ip'] = 'TAK server running on https://' + subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[1] + ':8443'
                subprocess.run(tak_enable.split(' '))
                subprocess.run(tak_start.split(' '))
                status['start_button_state'] = 'disabled'
                status['stop_button_state'] = 'active'
    else:
        status['message'] = 'TAK server not installed'
        status['start_button_state'] = 'disabled'
        status['stop_button_state'] = 'disabled'
    
def stop_tak():
    tak_stop = 'sudo systemctl start takserver.service'

    subprocess.run(tak_stop.split(' '))
    status['message'] = 'TAK server not running'
    status['start_button_state'] = 'active'
    status['stop_button_state'] = 'disabled'

