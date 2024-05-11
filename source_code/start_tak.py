import subprocess
import os
import cert_creation as cc

tak_status = 'service --status-all | grep "takserver"'
ip_check = 'ip addr show | grep -oE "inet (addr:)?([0-9]*\.){3}[0-9]*"'

status = {
    'message': '',
    'start_button_state': '',
    'stop_button_state': ''
}

def check_tak():
    if('tak' in os.listdir('/opt') and 'certs' in os.listdir('/opt/tak')):
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
                ips = subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')
                status['message'] = 'TAK Server on https://' + ips[len(ips)-2].split(' ')[1] + ':8443'
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
    
    print('\033[1;33m{}\033[0m'.format('starting TAK server...'))
    subprocess.run(tak_enable.split(' '))
    subprocess.run(tak_start.split(' '))

    os.chdir('/opt/tak/certs/files/admin_certs/')
    admin_certs_files = subprocess.run(['ls','-l'], stdout=subprocess.PIPE, text=True).stdout.split('\n')
    admin_p12_cert = ''
    for cert in admin_certs_files:
        if('tak_admin_{}.p12'.format(o_u) in cert.split(' ')):
            admin_p12_cert = cert
    if(user not in admin_p12_cert):
        subprocess.run(['sudo', 'chown', '-R', '{}:{}'.format(user,user), '/opt/tak/certs/files/admin_certs/tak_admin_{}.p12'.format(o_u)])
        print("\033[1;32mcopying admin .p12 certificate to the user's Desktop.\033[0m")
        subprocess.run(['sudo', 'cp', '-v', '/opt/tak/certs/files/admin_certs/tak_admin_{}.p12'.format(o_u), '/home/{}/Desktop'.format(user)])
        subprocess.run(['sudo', 'chown', '-R', '{}:{}'.format(user,user), '/home/{}/Desktop/tak_admin_{}.p12'.format(user, o_u)])
        def elevate_admin():
            elevate = subprocess.Popen(admin_cert_elevate, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            error = elevate.communicate()
            print('\033[1;33m{}\033[0m'.format('elevating admin cert, this may take some time...'))
            if(error and elevate.returncode != 0):
                # print(elevate.returncode)
                elevate_admin()
            elif(elevate.returncode == 0):
                # print(elevate.returncode)
                print('\033[1;32madmin account has been elevated.\033[0m')
        elevate_admin()
    ips = subprocess.run(ip_check, shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')
    status['message'] = 'TAK Server on https://' + ips[len(ips)-2].split(' ')[1] + ':8443'
    status['start_button_state'] = 'disabled'
    status['stop_button_state'] = 'active'
    print('\033[1;32m{}\033[0m'.format('successfully started TAK server.'))

    
def stop_tak():
    tak_stop = 'sudo systemctl stop takserver.service'

    print('\033[1;33mshutting down TAK server...\033[0m')
    subprocess.run(tak_stop.split(' '))
    status['message'] = 'TAK server not running'
    status['start_button_state'] = 'active'
    status['stop_button_state'] = 'disabled'
    print('\033[1;32m{}\033[0m\033[1;31m{}\033[0m\033[1;32m{}\033[0m'.format('successfully ', 'stopped ', 'TAK server.'))

