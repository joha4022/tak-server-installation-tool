# https://docs.python.org/3/library/tkinter.html
from tkinter import *
from tkinter import ttk
import cert_creation as cc
import install_frame as intf
import start_tak as st
import threading
import os


# widgets = button, input, etc.
# window = container that can hold widgets
# instantiate an instance of a window
window = Tk()
# window.geometry("400x200")
window.title("TAK Automation Tool")
frame = ttk.Frame(window)
frame.grid()

tak_status = StringVar()
meta_data = StringVar()
cert_status = StringVar()
user_cert_status = StringVar()
tak_status_text_bottom = StringVar()

state = StringVar()
city = StringVar()
org = StringVar()
org_unit = StringVar()
user_certs_quantity = IntVar()

tool_status = StringVar()

icon = PhotoImage(file = './resources/480px-USICorpsDUI.png')
window.iconphoto(False, icon)

### 1st frame: TAK START STOP
tak_frame = LabelFrame(frame)
tak_frame.grid(row=0, column=0, pady=(10,0), sticky='new', padx=20)

tak_start_b = ttk.Button(tak_frame, text='Start')
tak_start_b.grid(padx=10, sticky='e', row=0, column=0)
tak_start_b['command'] = lambda: [tool_progress('start','Starting TAK server...'),
                                  multi_thread(st.start_tak,())]
tak_stop_b = ttk.Button(tak_frame, text='Stop')
tak_stop_b.grid(padx=(0,10), sticky='e', row=0, column=1)
tak_stop_b['command'] = lambda: [tool_progress('start','Stopping TAK server...'),
                                  multi_thread(st.stop_tak,())]

tak_server_status_text = ttk.Label(tak_frame, textvariable=tak_status_text_bottom)
tak_server_status_text.grid(row=0, column=2, sticky='w', pady=(10,10))

def copy():
    window.clipboard_clear()
    window.clipboard_append(tak_status_text_bottom.get().split('on')[1])

address_copy = ttk.Button(tak_frame, text='copy')
address_copy.grid(row=0, column=3, sticky='e', pady=(10,10), padx=(10,10))
address_copy['command'] = lambda: [copy()]


### 2st frame: TAK INSTALLATION

# tak installation frame
tak_installation_frame = LabelFrame(frame, text='TAK Installation')
tak_installation_frame.grid(row=1, column=0, sticky='new', padx=20, pady=10)

# install and re-install buttons
b_install = ttk.Button(tak_installation_frame, text="Install")
b_install.grid(row=0, column=0, sticky='w', padx=10, pady=(0,10))
b_install['command'] = lambda: [multi_thread(intf.install_tak,())]

b_uninstall = ttk.Button(tak_installation_frame, text="Uninstall")
b_uninstall.grid(row=0, column=1, sticky='w', pady=(0,10))
b_uninstall['command'] = lambda: [tool_progress('start','Uninstalling TAK...'),
                                  multi_thread(intf.uninstall_tak,())]

# displays current version or status of the takserver
tak_installtation_status = ttk.Label(tak_installation_frame, textvariable=tak_status)
tak_installtation_status.grid(row=0, column=3, columnspan=20, sticky='w', padx=10, pady=(0,10))

### 3nd frame: ROOT CERTIFICATE INFORMATION

# root ca info frame
root_ca_info_frame = LabelFrame(frame, text='Root / Server / Admin Certificate(s)')
root_ca_info_frame.grid(row=2, column=0, sticky='news', padx=20, pady=10)

# cert information text
meta_data_label = ttk.Label(root_ca_info_frame, textvariable=meta_data)
meta_data_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)
cert_status_label = ttk.Label(root_ca_info_frame, textvariable=cert_status)
cert_status_label.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=(0,10))

# state box
ttk.Label(root_ca_info_frame, text='State').grid(row=2, column=0)
state_choice = ttk.Entry(root_ca_info_frame, textvariable=state)
state_choice.grid(row=3, column=0, padx=10, pady=(0,10))

# city box
ttk.Label(root_ca_info_frame, text = 'City').grid(row=2, column=1)
city_input = ttk.Entry(root_ca_info_frame, textvariable=city)
city_input.grid(row=3, column=1, padx=(0,10), pady=(0,10))

# organization box
ttk.Label(root_ca_info_frame, text = 'Organization').grid(row=2, column=2)
org_input = ttk.Entry(root_ca_info_frame, textvariable=org)
org_input.grid(row=3, column=2, padx=(0,10), pady=(0,10))

# organizational_unit box
ttk.Label(root_ca_info_frame, text = 'Organizational Unit').grid(row=4, column=0)
org_unit_input = ttk.Entry(root_ca_info_frame, textvariable=org_unit)
org_unit_input.grid(row=5, column=0, padx=10, pady=(0,10))

root_cert_generate_button = ttk.Button(root_ca_info_frame, text="Generate")
root_cert_generate_button.grid(row=6, column=0, sticky='w', padx=10, pady=(0,10))
root_cert_generate_button['command'] =lambda: [tool_progress('start','Creating admin, root, and server certificates...'),
                                               multi_thread(cc.generate, ('root', state.get(), city.get(), org.get(), org_unit.get(), user_certs_quantity.get()))]




### 4rd frame: USER CERTIFICATE INFORMATION

# user cert info frame
user_cert_info_frame = LabelFrame(frame, text='User Certificate(s)')
user_cert_info_frame.grid(row=3, column=0, sticky='news', padx=20)

# user cert information text
user_cert_info_label = ttk.Label(user_cert_info_frame, textvariable=user_cert_status)
user_cert_info_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)

# user cert quantity box
user_cert_label = ttk.Label(user_cert_info_frame, text = 'User Cert Quantity')
user_cert_label.grid(row=1, column=0, sticky='w', padx=10, pady=(0,10))
user_certs_quantity_input = ttk.Entry(user_cert_info_frame, textvariable=user_certs_quantity)
user_certs_quantity_input.grid(row=2, column=0, sticky='w', padx=10, pady=(0,10)) 

user_cert_generate_button = ttk.Button(user_cert_info_frame, text="Generate")
user_cert_generate_button['command'] = lambda: [tool_progress('start','Creating {} user certificate(s)...'.format(user_certs_quantity.get())), 
                                                multi_thread(cc.generate, ('user', state.get(), city.get(), org.get(), org_unit.get(), user_certs_quantity.get()))]
user_cert_generate_button.grid(row=3, column=0, sticky='w', padx=10, pady=(0,10))


### 5th frame: D2I
d2i_team = ttk.Label(frame, text='I Corps D2I Team')
d2i_team.grid(padx=20, sticky='e')

### 6th frame: CLOSE BUTTON

ttk.Button(frame, text='Close', command=window.destroy).grid(row=5, column=0)

### 7th frame: PROGRESS BAR

progress_bar_text = ttk.Label(textvariable=tool_status)
progress_bar_text.grid(row=6, column=0, sticky='news')

progress_bar = ttk.Progressbar(mode='determinate')
progress_bar.grid(row=7, column=0, sticky='news')




### functions 
def multi_thread(func, arg):
    thread = threading.Thread(target=func, args=arg)
    thread.start()
    
    def check_thread():
        if thread.is_alive():
            window.after(100, check_thread)
            if(intf.status['installation_started'] == True):
                tool_progress('start', 'Installing TAK...')
        else:
            refresh()
            tool_progress('stop', intf.status['tak_status'])
    check_thread()

def tool_progress(state, message):
    if (state == 'start'):
        tool_status.set(message)
        progress_bar.config(mode='indeterminate')
        progress_bar.start()
        window.update()
    elif (state == 'stop'):
        tool_status.set(message)
        progress_bar.config(mode='determinate')
        progress_bar.stop()

def disable_all():
    root_cert_generate_button.config(state='disabled')
    state_choice.config(state='disabled')
    city_input.config(state='disabled')
    org_input.config(state='disabled')
    org_unit_input.config(state='disabled')
    user_cert_generate_button.config(state='disabled')
    user_certs_quantity_input.config(state='disabled')

def refresh():
    st.check_tak()
    tak_status_text_bottom.set(st.status['message'])
    tak_start_b.config(state=st.status['start_button_state'])
    tak_stop_b.config(state=st.status['stop_button_state'])

    intf.tak_checker()
    b_install.config(state=intf.status['install_b'])
    b_uninstall.config(state=intf.status['uninstall_b'])
    tak_status.set(intf.status['tak_status'])

    cc.root_cert_checker()
    meta_data_status = 'C=' + cc.status['meta_data']['COUNTRY'] + ', S=' + cc.status['meta_data']['STATE'] + ', C=' + cc.status['meta_data']['CITY'] + ', O=' + cc.status['meta_data']['ORGANIZATION'] + ', OU=' + cc.status['meta_data']['ORGANIZATIONAL_UNIT']
    meta_data.set(meta_data_status)
    cert_status.set('Root Cert ' + cc.status['root_cert'] + '  Admin Cert ' + cc.status['admin_cert'] + '  Server Cert ' + cc.status['server_cert'])
    if('tak' in os.listdir('/opt')):
        if('files' in os.listdir('/opt/tak/certs')):
            files_folder = os.listdir('/opt/tak/certs/files')
            if('root-ca.pem' in files_folder and 'takserver.pem' in files_folder and 'admin_certs' in files_folder):
                root_cert_generate_button.config(state='disabled')
                state_choice.config(state='disabled')
                city_input.config(state='disabled')
                org_input.config(state='disabled')
                org_unit_input.config(state='disabled')
                user_cert_generate_button.config(state='active')
                user_certs_quantity_input.config(state='active')
                cc.user_cert_checker()
                user_cert_status.set('Total of ' + str(cc.status['user_certs']) + ' User certfications')
        else:
            root_cert_generate_button.config(state='active')
            state_choice.config(state='active')
            city_input.config(state='active')
            org_input.config(state='active')
            org_unit_input.config(state='active')
            user_cert_generate_button.config(state='disabled')
            user_certs_quantity_input.config(state='disabled')
            user_cert_status.set('Create root/server/admin certificates before generating user certificate(s).')
    else:
        user_cert_status.set('TAK server not installed')
        disable_all()

    state.set('')
    city.set('')
    org.set('')
    org_unit.set('')
    user_certs_quantity.set(0)
    tool_status.set(intf.status['tak_status'])

### executions
refresh()

# place window on computer screen and listens for events
window.mainloop()
