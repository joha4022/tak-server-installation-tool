# tak-automation
TAK Automation is a tool that automates TAK server installation, deletion, and certificates with a basic GUI using Tkinter. <br><br>
**Note: This is still in production and only been tested with TAK server version 5.0, 5.1 & ubuntu 22.04.3 LTS**

## To Start
1. Clone or download this repository and open up a terminal. <br>
2. Navigate to the exe folder and the exe file using sudo: ```sudo ./exe```

## Functionalities
There are 4 main functionalities to the TAK Automation, which are:

### 1. TAK server installation and & uninstallation
Requirement: Ubuntu OS, TAK .deb file, and internet connection (for initial installation if the OS is brand new)

Depending on the state of the OS, it will install Java and Postgres which are required resources to install and run a TAK server. TAK uninstallation will remove TAK and the folders that are associated with it but it will not remove Java or Postgres installation. After a user has installed TAK once using this method, the user should be able to re-install TAK without an internet connection.

Upcoming features: UI - The TAK automation will check whether the user has an internet connection and a checker for Java and Postgres.

### 2. TAK server root/admin/server certificate creation
Requirement: TAK server is installed

Users are required to input fields such as STATE, CITY, ORGANIZATION, and ORGANIZATIONAL UNIT, it will generate TAK server root, admin, and server certificates based on the information provided by the users.

TAK certs are stored in /opt/tak/certs/files

### 3. Start TAK server
Requirement: root/admin/server certificates are generated

The initial start of the TAK server will elevate the admin certificate created in step 3 and it will make a copy of an admin cert on the user's desktop. **The user will still have to follow the manual process of importing the admin cert to the browser and edit the trust.** If you are unfamiliar with this step, please follow the link below and look at **The Administrative Dashboard.** Once the TAK server is running, on the tak-automation UI, it will display the ip and the port used for the TAK server.

https://mytecknet.com/lets-build-a-tak-server/#the-administrative-dashboard

### 4. TAK user certificate creation
Requirement: TAK server root/admin/server certificates

Users can create multiple user certificates by entering the required certificate quantity. TAK Automation tool will create individual user certificate folders "user_certs_#" and store them inside /opt/tak/certs/files/user_certs and to the user's desktop. Users can continue to generate additional user certificates by repeating the same process. The user certificate numbering will increment as more user certificates are generated.


