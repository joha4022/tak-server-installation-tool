import subprocess
import in_place
import os

s = ''
c = ''
o = ''
o_u = ''
q = 0

status = {
            'meta_data': {
                'COUNTRY': 'N/A',
                'STATE':'N/A',
                'CITY':'N/A',
                'ORGANIZATION':'N/A',
                'ORGANIZATIONAL_UNIT':'N/A'
            },
            'root_cert': '[ ]',
            'server_cert': '[ ]',
            'admin_cert': '[ ]',
            'user_certs': 0
        }

def root_cert_checker():
    if('tak' in os.listdir('/opt') and 'certs' in os.listdir('/opt/tak') and 'files' in os.listdir('/opt/tak/certs')):
        print('\033[1;33m{}\033[0m'.format('checking certificate meta data...'))
        with open('/opt/tak/certs/cert-metadata.sh', 'r') as meta_data:
            for line in meta_data:
                if 'COUNTRY=' in line:
                    status['meta_data']['COUNTRY'] = line.split('=')[1].strip()
                if 'STATE=' in line:
                    state = (lambda: ' ' if '$' in line.split('=')[1] else line.split('=')[1])()
                    status['meta_data']['STATE'] = state.strip()
                if 'CITY=' in line:
                    city = (lambda: ' ' if '$' in line.split('=')[1] else line.split('=')[1])()
                    status['meta_data']['CITY'] = city.strip()
                if 'ORGANIZATION=' in line:
                    org = (lambda: ' ' if '$' in line.split('=')[1] else line.split('=')[1])()
                    status['meta_data']['ORGANIZATION'] = org.strip()
                if 'ORGANIZATIONAL_UNIT=' in line:
                    org_unit = (lambda: ' ' if '$' in line.split('=')[1] else line.split('=')[1])()
                    status['meta_data']['ORGANIZATIONAL_UNIT'] = org_unit.strip()
        tak_files = os.listdir('/opt/tak/certs/files')
        status['root_cert'] = (lambda: '[x]' if 'root-ca.pem' in tak_files else '[ ]')()
        status['admin_cert'] = (lambda: '[x]' if 'admin_certs' in tak_files else '[ ]')()
        status['server_cert'] = (lambda: '[x]' if 'takserver.pem' in tak_files else '[ ]')()
        print('\033[1;32mupdated all certificate status.\033[0m')
    else:
        status['meta_data']['COUNTRY'] = 'N/A'
        status['meta_data']['STATE'] = 'N/A'
        status['meta_data']['CITY'] = 'N/A'
        status['meta_data']['ORGANIZATION'] = 'N/A'
        status['meta_data']['ORGANIZATIONAL_UNIT'] = 'N/A'
        status['root_cert'] = '[ ]'
        status['server_cert'] = '[ ]'
        status['admin_cert'] = '[ ]'

def user_cert_checker():
    if('tak' in os.listdir('/opt')):
        if('files' in os.listdir('/opt/tak/certs')):
            if('user_certs' in os.listdir('/opt/tak/certs/files')):
                print('\033[1;33m{}\033[0m'.format('checking user certificate status...'))
                user_certs = os.listdir('/opt/tak/certs/files/user_certs')
                status['user_certs'] = len(user_certs)
                print('\033[1;32m{}\033[0m'.format('updated user certificate status.'))
    else:
        status['user_certs'] = 0

def edit_meta_data():
    print(s, c, o, o_u)
    if s and c and o and o_u != "" :
        with in_place.InPlace("/opt/tak/certs/cert-metadata.sh") as cert_meta_data:
            for line in cert_meta_data:
                cert_meta_data.write(
                    'STATE={}\n'.format(s) if 'STATE=' in line else
                    'CITY={}\n'.format(c) if 'CITY=' in line else
                    'ORGANIZATION={}\n'.format(o) if 'ORGANIZATION=' in line else
                    'ORGANIZATIONAL_UNIT={}\n'.format(o_u) if 'ORGANIZATIONAL_UNIT=' in line else
                    line)
        print('\033[1;32mcert-metadata.sh file has been updated.\033[0m')
        subprocess.run(['sudo', 'chown', '-R', 'tak:tak', '/opt/tak/'])
    else: 
        print('\033[1;31please complete all fields.\033[0m')

def make_root_ca():
    root_ca = 'TAK_ROOT_CA_{}'.format(o_u)
    os.chdir('/opt/tak/certs/')
    subprocess.run(['./makeRootCa.sh', '--ca-name', root_ca], stdout=subprocess.PIPE)
    print('\033[1;32m{}\033[0m'.format('created root certificate: {}.'.format(root_ca)))
    # add feature to print where the cert was created & name of the cert

def make_server_cert():
    subprocess.run(['./makeCert.sh', 'server', 'takserver'], stdout=subprocess.PIPE)
    print('\033[1;32m{}\033[0m'.format('created server certificate: takserver'))

def make_admin_certs():
    file_path = '/opt/tak/certs/files/'

    # create separate folder for admin certs
    os.mkdir('/opt/tak/certs/files/admin_certs')
    os.chdir('/opt/tak/certs')
    subprocess.run(['./makeCert.sh', 'client', 'tak_admin_{}'.format(o_u)], stdout=subprocess.PIPE)
    subprocess.run(['mv', 
                        '{}tak_admin_{}.csr'.format(file_path, o_u), 
                        '{}tak_admin_{}.key'.format(file_path, o_u), 
                        '{}tak_admin_{}.p12'.format(file_path, o_u), 
                        '{}tak_admin_{}.pem'.format(file_path, o_u), 
                        '{}tak_admin_{}-trusted.pem'.format(file_path, o_u), 
                        '{}tak_admin_{}.jks'.format(file_path, o_u), '-t', '{}admin_certs'.format(file_path) ])
    print('\033[1;32m{}\033[0m'.format('created admin certificate: tak_admin_{}.'.format(o_u)))

def make_user_certs():
    user = os.listdir('/home')[0]
    file_path = '/opt/tak/certs/files/'
    # check if user_certs folder exists, if not, create.
    check_user_certs_folder = os.listdir('/opt/tak/certs/files')
    if('user_certs' not in check_user_certs_folder):
        # create separate folder for all user certs within certs/files folder
        os.mkdir('/opt/tak/certs/files/user_certs')
        # if user certs folder do not exist on the desktop create
        if('user_certs' not in os.listdir('/home/{}/Desktop'.format(user))):
            os.mkdir('/home/{}/Desktop/user_certs'.format(user))
        for count in range(1,q + 1):
            os.chdir('/opt/tak/certs/files')
            os.mkdir('user_{}'.format(count))
            os.chdir('/opt/tak/certs')
            subprocess.run(['./makeCert.sh', 'client', 'user_{}'.format(count)], stdout=subprocess.PIPE)
            subprocess.run(['mv', 
                            '{}user_{}.csr'.format(file_path, count), 
                            '{}user_{}.key'.format(file_path, count), 
                            '{}user_{}.p12'.format(file_path, count), 
                            '{}user_{}.pem'.format(file_path, count), 
                            '{}user_{}-trusted.pem'.format(file_path, count), 
                            '{}user_{}.jks'.format(file_path, count), '-t', '{}user_{}'.format(file_path, count) ])
            subprocess.run(['mv', '{}user_{}'.format(file_path, count), '-t', '{}/user_certs'.format(file_path)])
            subprocess.run(['sudo', 'cp', '-r', '{}user_certs/user_{}'.format(file_path, count),  '/home/{}/Desktop/user_certs'.format(user)])
            print('\033[1;32mcreated user_{} certificates.\033[0m'.format(count))
    else:  
        # check for exisiting user certs
        existing_user_certs = os.listdir('/opt/tak/certs/files/user_certs')
        for count in range(len(existing_user_certs) + 1,q + len(existing_user_certs) + 1):
            os.chdir('/opt/tak/certs/files')
            os.mkdir('user_{}'.format(count))
            os.chdir('/opt/tak/certs')
            subprocess.run('./makeCert.sh client user_{}'.format(count), shell=True, stdout=subprocess.PIPE)
            subprocess.run(['mv', 
                            '{}user_{}.csr'.format(file_path, count), 
                            '{}user_{}.key'.format(file_path, count), 
                            '{}user_{}.p12'.format(file_path, count), 
                            '{}user_{}.pem'.format(file_path, count), 
                            '{}user_{}-trusted.pem'.format(file_path, count), 
                            '{}user_{}.jks'.format(file_path, count), '-t', '{}user_{}'.format(file_path, count) ])
            subprocess.run(['sudo', 'cp', '-r', '{}user_{}'.format(file_path, count),  '/home/{}/Desktop/user_certs'.format(user)])
            subprocess.run(['mv', '{}user_{}'.format(file_path, count), '-t', '{}/user_certs'.format(file_path)])
            print('\033[1;32mcreated user_{} certificates.\033[0m'.format(count))
    # check if permission change is necessary 
    # subprocess.run('sudo chown -R {}:{} /home/{}/Desktop/user_certs'.format(user, user, user), shell=True)

def generate(type, state, city, org, org_u, quant):
    global s, c, o, o_u, q
    s = state.replace(" ", "_")
    c = city.replace(" ", "_")
    o = org.replace(" ", "_")
    o_u = org_u.replace(" ", "_")
    q = quant

    if(type == 'root'):
        edit_meta_data()
        make_root_ca()
        make_server_cert()
        make_admin_certs()
        root_cert_checker()
    elif(type == 'user'):
        make_user_certs()
        user_cert_checker()