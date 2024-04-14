from tkinter import *
from tkinter.filedialog import askopenfile
import subprocess
import os

status = {
        'install_b': 'active',
        'uninstall_b': 'disabled',
        'tak_status': '',
        'installation_started': False
    }

def install_tak():
    # install WINTAK
    os.chdir('/home')
    deb_file = askopenfile(mode='r', filetypes=[('.Deb file', '*.deb')])
    if deb_file:
        status['installation_started'] = True

        filename = os.path.abspath(deb_file.name).split('/')[-1]
        complete_filepath = os.path.abspath(deb_file.name).split('/')
        complete_filepath.pop(-1)
        filepath = '/'.join(complete_filepath)

        # check for java
        check_java = subprocess.run(['sudo','java', '-version'], stderr=subprocess.PIPE, universal_newlines=True).stderr.split('\n')
        if('openjdk' not in check_java[0]):
            subprocess.run(['sudo', 'apt', 'install', 'default-jre'], input=b'y\n')
            print('\n///////// {} installed. //////////'.format(check_java[0]))
        else:
            print('////////// current version of java: {}. //////////'.format(check_java[0]))

        # check for keyrings folder
        check_keyrings_dir = subprocess.run(['ls'], cwd='/etc/apt', stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        if('keyrings' not in check_keyrings_dir):
            os.mkdir('/etc/apt/keyrings')
            print('\n////////// created /etc/apt/keyrings directory. //////////')
        else:
            print('\n////////// /etc/apt/keyrings directory exists. //////////')
        
        # check for curl
        check_curl = subprocess.run(['sudo', 'apt', 'list', '--installed', 'curl'], stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        if('curl' not in check_curl[1]):
            subprocess.run(['sudo','apt','install','curl'])
            print('\n////////// curl installed.  //////////')

        # install postgresql
        check_keyrings_dir = subprocess.run(['ls'], cwd='/etc/apt/keyrings', stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        check_postgresql = subprocess.run(['sudo', 'apt', 'list', '--installed', 'postgresql-15'], stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        if('postgresql.asc' not in check_keyrings_dir or 'postgresql-15' not in check_postgresql[1]):
            install_postgres1 = 'sudo curl https://www.postgresql.org/media/keys/ACCC4CF8.asc --output /etc/apt/keyrings/postgresql.asc'
            install_postgres2 = "'"'echo "deb [signed-by=/etc/apt/keyrings/postgresql.asc] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" /etc/apt/sources.list.d/postgresql.list'"'"
            subprocess.run(install_postgres1.split(' '))
            test = subprocess.run(['sudo', 'sh', '-c', install_postgres2])
            print(' '.join(test.args))
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install', 'postgresql-15'])
            # subprocess.run(['sudo', 'apt', 'upgrade'], input=b'y\n')
            if('postgresql-15' in check_postgresql[1]):
                print('\n////////// postgresql installed. //////////')
        else:
            print('\n////////// postgresql exists. //////////')

        if('postgresql-15' in check_postgresql[1]): 
            os.chdir(filepath)
            # wait for the process to be processed for a bit and wait until it shows a prompt and THEN press y.
            subprocess.run(['sudo', 'apt', 'install', './{}'.format(filename)], input=b'y\n')
            print('\n////////// TAK installation complete. //////////')
            status['installation_started'] = False
            tak_checker()
        else:
            print('\n////////// TAK installation could not be installed. //////////')
            status['installation_started'] = False

def uninstall_tak():
    # stop takserver
    subprocess.run(['sudo', 'systemctl', 'stop', 'takserver'])
    # kill all processes related to takserver
    subprocess.run(['sudo', 'killall','-9','takserver'])
    # kill all java related processes
    subprocess.run(['sudo', 'killall','-9','java'])
    # uninstall takserver
    subprocess.run(['sudo', 'apt', 'remove', '--purge', 'takserver'], input=b'y\n')
    # remove tak folder from /opt
    subprocess.run(['sudo', 'rm', '-rf', '/opt/tak'])

    print('\n////////// TAK uninstallation complete //////////')
    tak_checker()

def tak_checker():
    # see if takserver can be found as one of the installed application
    check_for_tak = subprocess.run(['sudo', 'apt', 'list', '--installed', 'takserver'], stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')

    if('takserver' in check_for_tak[1]):
        version = check_for_tak[1].split(' ')[1]

        status['uninstall_b'] = 'active'
        status['install_b'] = 'disabled'
        status['tak_status'] = 'TAK Version: ' + version
    else:
        status['uninstall_b'] = 'disabled'
        status['install_b'] = 'active'
        status['tak_status'] = 'Click "Install" and select the TAK *.deb file to start the installation.'
