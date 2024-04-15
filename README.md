# tak-automation
TAK Automation is a tool that automates WINTAK or TAK server installation, deletion, and certificates with a basic GUI using Tkinter.

## To Start
1. Clone the this repository and open up a terminal. <br>
2. To run the tak-automation application, navigate to the directory where the tak-automation.exe file is and type: ```sudo ./tak-automation```

## Functionalities
There are 3 main functionalities to the TAK Automation, which are:

### 1. TAK installation and & uninstallation
Requirement: Ubuntu OS, TAK .deb file, and internet connection (for initial installation if the OS is brand new)
Depending on the state of the OS, it will install Java and Postgres which are required resources to install and run a TAK server. TAK uninstallation will remove TAK and the folders that are associated with it but it will not remove Java or Postgres installation. After a user has installed TAK once using this method, the user should be able to re-install TAK without an internet connection.

Upcoming features: UI - The TAK automation will check whether the user has an internet connection and a checker for Java and Postgres.

### 2. TAK server root/admin/server certificate creation
Requirement: TAK server is installed
Users are required to input fields such as STATE, CITY, ORGANIZATION, and ORGANIZATIONAL UNIT, it will generate TAK server root, admin, and server certificates based on the information provided by the users.

TAK certs are stored in /opt/tak/certs/files

### 3. TAK user certificate creation
Requirement: TAK server root/admin/server certificates
Users can create multiple user certificates by entering the required certificate quantity. TAK Automation tool will create individual user certificate folders "user_certs_#" and store them inside /opt/tak/certs/files/user_certs. Users can continue to generate additional user certificates by repeating the same process. The user certificate numbering will increment as more user certificates are generated.
