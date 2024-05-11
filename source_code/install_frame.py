from tkinter import *
from tkinter.filedialog import askopenfile
import subprocess
import os

user = os.listdir('/home')[0]

status = {
        'install_b': 'active',
        'uninstall_b': 'disabled',
        'tak_status': '',
        'installation_started': False
    }

def online_install_tak(deb_file):
    # # install TAK server
    # os.chdir('/home/{}'.format(user))
    # deb_file = askopenfile(mode='r', filetypes=[('.Deb file', '*.deb')])
    if deb_file:

        filename = os.path.abspath(deb_file.name).split('/')[-1]
        complete_filepath = os.path.abspath(deb_file.name).split('/')
        complete_filepath.pop(-1)
        filepath = '/'.join(complete_filepath)

        subprocess.run(['sudo', 'apt-get', 'update'], stdout=subprocess.PIPE)

        # check for java
        check_java = subprocess.run('sudo dpkg -l openjdk-11*', shell=True, stdout=subprocess.PIPE)
        if(check_java.returncode != 0):
            print('\033[1;33minstalling openjdk-11-jre-headless...\033[0m')
            subprocess.run(['sudo', 'apt-get', 'install', 'openjdk-11-jre-headless'], input=b'y\n')
            print('\033[1;32mopenjdk-11-jre-headless was installed.\033[0m')

        # check for keyrings folder
        check_keyrings_dir = subprocess.run(['ls'], cwd='/etc/apt', stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        if('keyrings' not in check_keyrings_dir):
            print('\033[1;33mcreating /etc/apt/keyrings directory...\033[0m')
            os.mkdir('/etc/apt/keyrings')
            print('\033[1;32mcreated /etc/apt/keyrings directory.\033[0m')
        
        # check for curl
        check_curl = subprocess.run('sudo dpkg -l curl', shell=True, stdout=subprocess.PIPE)
        if(check_curl.returncode != 0):
            print('\033[1;33minstalling curl...\033[0m')
            subprocess.run(['sudo','apt-get','install','curl'], input=b'y\n')
            print('\033[1;32mcurl was installed.\033[0m')

        # install postgresql
        check_keyrings_dir = subprocess.run(['ls'], cwd='/etc/apt/keyrings', stdout=subprocess.PIPE, universal_newlines=True).stdout.split('\n')
        check_postgresql = subprocess.run('sudo dpkg -l postgresql-15', shell=True, stdout=subprocess.PIPE)
        if('postgresql.asc' not in check_keyrings_dir or check_postgresql.returncode != 0):
            install_postgres1 = 'sudo curl https://www.postgresql.org/media/keys/ACCC4CF8.asc --output /etc/apt/keyrings/postgresql.asc'
            install_postgres2 = 'sudo sh -c \'echo "deb [signed-by=/etc/apt/keyrings/postgresql.asc] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/postgresql.list\''
            print('\033[1;33minstalling postgresql-15...\033[0m')
            subprocess.run(install_postgres1.split(' '))
            subprocess.run(install_postgres2, shell=True)
            subprocess.run('sudo apt-get install postgresql-15 -y', stdout=subprocess.PIPE, shell=True)
            print('\033[1;32mpostgresql-15 installed.\033[0m')

        os.chdir(filepath)
        # wait for the process to be processed for a bit and wait until it shows a prompt and THEN press y.
        print('\033[1;33minstalling TAK server...\033[0m')
        install_tak_command = subprocess.run('sudo apt-get install ./{} -y'.format(filename), shell=True)
        if(install_tak_command.returncode == 0):
            print('\033[1;32m{}\033[0m'.format('successfully installed TAK server.'))
        else:
            print('\031[1;32m{}\033[0m'.format('something went wrong, please try again.'))
        print('\033[1;32m{}\033[0m'.format('running tak checker.'))
        status['installation_started'] = False
        tak_checker()

def offline_install_tak(deb_file):
    # # install wintak server using offline method
    # os.chdir('/home/{}'.format(user))
    # deb_file = askopenfile(mode='r', filetypes=[('.Deb file', '*.deb')])
    if deb_file:

        filename = os.path.abspath(deb_file.name).split('/')[-1]
        complete_filepath = os.path.abspath(deb_file.name).split('/')
        complete_filepath.pop(-1)
        filepath = '/'.join(complete_filepath)
        rf = ('/').join(subprocess.run('find /home -name "offline-update.tar.gz"', shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')[0].split('/')[:-1])
        # do initial update
        print('\033[1;33mextracting and transferring offline ubuntu update files...\033[0m')
        subprocess.run('sudo tar -xf {}/offline-update.tar.gz -C {}/'.format(rf, rf), shell=True)
        # fix this to /var/lib/apt/lists
        subprocess.run('sudo cp -a {}/offline-update/. /var/lib/apt/lists'.format(rf), shell=True)
        print('\033[1;32minitial update complete.\033[0m')

        # check for java
        check_java = subprocess.run('sudo dpkg -l openjdk-11*', shell=True, stdout=subprocess.PIPE)
        if(check_java.returncode != 0):
            print('\033[1;33minstalling openjdk-11-jre-headless...\033[0m')
            subprocess.run('sudo tar -xf {}/openjdk-11-jre-headless.tar.gz -C {}/'.format(rf, rf), shell=True)
            subprocess.run('sudo dpkg -i {}/openjdk-11-jre-headless/*.deb'.format(rf), shell=True)
            print('\033[1;32mopenjdk-11-jre-headless was installed.\033[0m')

        # install postgresql
        check_postgresql = subprocess.run('sudo dpkg -l postgresql-15', shell=True, stdout=subprocess.PIPE)
        if(check_postgresql.returncode != 0):
            print('\033[1;33minstalling postgresql-15...\033[0m')
            subprocess.run('sudo tar -xf {}/postgresql-15.tar.gz -C /'.format(rf,rf), shell=True)
            subprocess.run('sudo dpkg -i {}/postgresql-15/*.deb'.format(rf), shell=True)
            print('\033[1;32mpostgresql-15 installed.\033[0m')

        # install takserver dependencies
        print('\033[1;33minstalling takserver dependencies...\033[0m')
        subprocess.run('sudo tar -xf {}/takserver_5.x-packages.tar.gz -C {}/'.format(rf,rf), shell=True)
        subprocess.run('sudo dpkg -i {}/takserver_5.x-packages/*.deb'.format(rf), shell=True)
        print('\033[1;32mtakserver dependencies installed.\033[0m')

    os.chdir(filepath)
    # wait for the process to be processed for a bit and wait until it shows a prompt and THEN press y.
    print('\033[1;33minstalling TAK server...\033[0m')
    install_tak_command = subprocess.run(['sudo', 'apt', 'install', './{}'.format(filename)], input=b'y\n')
    if(install_tak_command.returncode == 0):
        print('\033[1;32minstalled TAK server successfully.\033[0m')
    else:
        print('\031[1;32msomething went wrong, please try again.\033[0m')
    status['installation_started'] = False
    tak_checker()

def install_tak():
    # install wintak server using offline method
    os.chdir('/home/{}'.format(user))
    deb_file = askopenfile(mode='r', filetypes=[('.Deb file', '*.deb')])
    if(deb_file):
        status['installation_started'] = True
        print('\033[1;33mtesting internet connection...\033[0m')
        ping_ubuntu_server = subprocess.run('ping -c 4 us.archive.ubuntu.com', shell=True, stdout=subprocess.PIPE, text=True)
        ping_postgresql_server = subprocess.run('ping -c 4 apt.postgresql.org', shell=True, stdout=subprocess.PIPE, text=True)
        if(ping_ubuntu_server.returncode == 2 or ping_postgresql_server == 2):
            print('\033[1;31mfailed to connect to ubuntu & postgresql archive server.\033[0m')
            print('\033[1;33mproceeding with offline installation...\033[0m')
            offline_install_tak(deb_file)
        else:
            print('\033[1;33mproceeding with online installation...\033[0m')
            online_install_tak(deb_file)

def uninstall_tak():
    # stop takserver
    subprocess.run(['sudo', 'systemctl', 'stop', 'takserver'])
    subprocess.run(['sudo', 'systemctl', 'disable', 'takserver'])

    # kill all processes related to takserver
    subprocess.run(['sudo', 'killall','-9','takserver'])
    # kill all java related processes
    subprocess.run(['sudo', 'killall','-9','java'])

    def purge_tak():
        # uninstall takserver
        purge = subprocess.run(['sudo', 'apt', 'remove', '--purge', 'takserver'], input=b'y\n')
        if(purge and purge.returncode != 0):
            purge_tak()
        else:
            # remove tak folder from /opt
            subprocess.run(['sudo', 'rm', '-rf', '/opt/tak'])
            subprocess.run('sudo rm -rf /home/{}/Desktop/user_certs'.format(user), shell=True)
            tak_checker()
            print('\033[1;32msuccessfully\033[0m \033[1;31muninstalled\033[0m \033[1;32mTAK server.\033[0m')
    purge_tak()

def tak_checker():
    # see if takserver can be found as one of the installed application
    check_for_tak = subprocess.run(['sudo', 'dpkg', '-l', 'takserver*'], stdout=subprocess.PIPE, universal_newlines=True)

    if(check_for_tak.returncode == 0):
        version = check_for_tak.stdout.split('\n')[5].split(' ')[8]

        status['uninstall_b'] = 'active'
        status['install_b'] = 'disabled'
        status['tak_status'] = 'TAK Version: ' + version
    else:
        status['uninstall_b'] = 'disabled'
        status['install_b'] = 'active'
        status['tak_status'] = ' '
