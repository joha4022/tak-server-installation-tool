import subprocess
import os
import cert_creation as cc
import time

tak_status = 'service --status-all | grep "takserver"'
ip_check = 'ip addr show | grep -oE "inet (addr:)?([0-9]*\.){3}[0-9]*"'

status = {
    'message': '',
    'start_button_state': '',
    'stop_button_state': ''
}

def check_tak():
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
                status['message'] = 'TAK server on https://' + subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[1].split(' ')[1] + ':8443'
                status['start_button_state'] = 'disabled'
                status['stop_button_state'] = 'active'
    else:
        status['message'] = 'TAK server not installed'
        status['start_button_state'] = 'disabled'
        status['stop_button_state'] = 'disabled'
    


def start_tak():
    tak_enable = 'sudo systemctl enable takserver.service'
    tak_start = 'sudo systemctl start takserver.service'
    user = os.listdir('/home')[0]
    o_u = cc.status['meta_data']['ORGANIZATIONAL_UNIT']
    admin_cert_elevate = 'sudo java -jar /opt/tak/utils/UserManager.jar certmod -A /opt/tak/certs/files/admin_certs/tak_admin_{}.pem'.format(o_u)
    
    print("\n////////// starting TAK server //////////")
    subprocess.run(tak_enable.split(' '))
    subprocess.run(tak_start.split(' '))

    os.chdir('/opt/tak/certs/files/admin_certs/')
    admin_certs_files = subprocess.run(['ls','-l'], stdout=subprocess.PIPE, text=True).stdout.split('\n')
    admin_p12_cert = ''
    for cert in admin_certs_files:
        if('{}.p12' in cert):
            admin_p12_cert = cert
    if(user not in admin_p12_cert):
        subprocess.run(['sudo', 'chown', '-R', '{}:{}'.format(user,user), '/opt/tak/certs/files/admin_certs/tak_admin_{}.p12'.format(o_u)])
        print("\n////////// copying admin .p12 certifcate to the user's Desktop //////////")
        subprocess.run(['sudo', 'cp', '-v', '/opt/tak/certs/files/admin_certs/tak_admin_{}.p12'.format(o_u), '/home/{}/Desktop'.format(user)])
        subprocess.run(['sudo', 'chown', '-R', '{}:{}'.format(user,user), '/home/{}/Desktop/tak_admin_{}.p12'.format(user, o_u)])
        def elevate_admin():
            elevate = subprocess.Popen(admin_cert_elevate, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if(elevate.returncode != 0):
                print(elevate.returncode)
                print('there was an error')
                elevate_admin()
            else:
                print(elevate.returncode)
                print('admin account has been elevated')
        elevate_admin()
        
    
    status['message'] = 'TAK server on https://' + subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[1].split(' ')[1] + ':8443'
    status['start_button_state'] = 'disabled'
    status['stop_button_state'] = 'active'

    
def stop_tak():
    tak_stop = 'sudo systemctl stop takserver.service'

    print("\n////////// shutting down TAK server //////////") 
    subprocess.run(tak_stop.split(' '))
    status['message'] = 'TAK server not running'
    status['start_button_state'] = 'active'
    status['stop_button_state'] = 'disabled'

