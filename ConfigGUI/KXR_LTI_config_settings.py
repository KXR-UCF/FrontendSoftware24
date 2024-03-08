from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import colorchooser
import os
import socket
import tv_communication as tv



# Wanda info
PRINT_SENSORS_COMMAND = 0x55000000
ADD_SENSOR_COMMAND = 0xCF000000
wandaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
# Wanda connection
try:
    wandaSocket.connect(('192.168.1.10', 35912))
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)
"""


# Classes
# object for each channel row
class adc_channel:
    def __init__(self, index):
        self.index = index
        self.data_channel = 0
        self.data_type = 0
        self.data_type_name = 0
        self.data_unit = 0
        self.data_serial = 0
        
        self.entry_channel = 0
        self.entry_type = 0
        self.entry_type_name = 0
        self.entry_unit = 0
        self.entry_serial = 0
        
        self.color_code = 0
        self.color_button = 0
    
    # creates a new adc channel row
    def create_widget(self, num_channels):
        # channel
        self.data_channel = StringVar()
        self.data_channel.set(' ')
        self.entry_channel = ttk.Combobox(wanda_sframe, values=wanda_adc_channel_values, state='readonly', textvariable=self.data_channel, postcommand=self.prev_channel_selection)
        self.entry_channel.bind('<<ComboboxSelected>>', self.next_channel_selection)
        self.entry_channel.grid(row=num_channels+4, column=0, padx=padding, pady=padding)
        # type
        self.data_type = StringVar()
        self.entry_type = ttk.Combobox(wanda_sframe, values=wanda_adc_type_values, state='readonly', textvariable=self.data_type)
        self.entry_type.bind('<<ComboboxSelected>>', self.type_selection)
        self.entry_type.grid(row=num_channels+4, column=1, padx=padding, pady=padding)
        # type name
        self.data_type_name = StringVar()
        self.entry_type_name = ttk.Combobox(wanda_sframe, values=[' '], state='readonly', textvariable=self.data_type_name)
        self.entry_type_name.bind('<<ComboboxSelected>>', self.type_update)
        self.entry_type_name.grid(row=num_channels+4, column=2, padx=padding, pady=padding)
        # unit
        self.data_unit = StringVar()
        self.entry_unit = ttk.Combobox(wanda_sframe, values=wanda_adc_unit_values, state='readonly', textvariable=self.data_unit)
        self.entry_unit.grid(row=num_channels+4, column=3, padx=padding, pady=padding)
        # serial
        self.data_serial = StringVar()
        self.entry_serial = Entry(wanda_sframe, textvariable=self.data_serial, state='readonly')
        self.entry_serial.grid(row=num_channels+4, column=4, padx=padding, pady=padding)
        # color
        self.color_code = '#000000'
        self.color_button = Button(wanda_sframe, text='Color', command=self.choose_color)
        self.color_button.grid(row=num_channels+4, column=5, padx=padding, pady=padding)

    # destroys last adc row
    def destroy_widget(self):
        # just need to destroy actual widgets
        self.entry_channel.destroy()
        self.entry_type.destroy()
        self.entry_type_name.destroy()
        self.entry_unit.destroy()
        self.entry_serial.destroy()
        self.color_button.destroy()

    # makes sure that there are no duplicate channels selected
    def next_channel_selection(self, event):
        global prev_selection
        global wanda_adc_channel_values
        global wanda_adc_channel_checker
        
        if self.entry_channel.current() == 0:
            # doesn't matter
            prev_selection = 0
        elif wanda_adc_channel_checker[self.entry_channel.current()] == 0:
            # valid selection
            wanda_adc_channel_checker[self.entry_channel.current()] = self.index
        else:
            # invalid selection
            self.data_channel.set(wanda_adc_channel_values[prev_selection])
            wanda_adc_channel_checker[prev_selection] = self.index

    # grabs the previously selected item of Combobox (index)
    def prev_channel_selection(self):
        global prev_selection
        global wanda_adc_channel_checker
        # save the previous and update checker
        prev_selection = self.entry_channel.current()
        wanda_adc_channel_checker[prev_selection] = 0
    
    # grabs the color as hex
    def choose_color(self):
        temp = self.color_code
        self.color_code = colorchooser.askcolor(title ='Choose color')[1]
        if self.color_code is None:
            self.color_code = temp
        self.color_button.config(bg=self.color_code)
    
    # set type name values based on type
    def type_selection(self, event):
        if self.entry_type.current() == 0:
            self.entry_type_name.config(values=wanda_adc_pressure_values)
        if self.entry_type.current() == 1:
            self.entry_type_name.config(values=wanda_adc_load_values)
        if self.entry_type.current() == 2:
            self.entry_type_name.config(values=wanda_adc_thermo_values)
        self.entry_type_name.current(0)
        self.data_serial.set(self.entry_type_name.current())
    
    # set type name update
    def type_update(self, event):
        self.data_serial.set(self.entry_type_name.current())



# object for the list of channel rows
class adc_channel_list:
    def __init__(self):
        self.adc_channels = []
        self.num_channels = 0
    
    # adds adc channel rows based on loop_count
    def add_channel(self, loop_count):
        for i in range(loop_count):
            # stay in range
            if self.num_channels < 40:
                self.adc_channels.append(adc_channel(self.num_channels)) # add to list
                self.adc_channels[self.num_channels].create_widget(self.num_channels) # create tkinter widgets
                self.num_channels += 1 # here for proper indexing
    
    # deletes adc channel rows based on loop_count
    def delete_channel(self, loop_count):        
        for i in range(loop_count):
            # stay in range
            if self.num_channels > 1:
                self.num_channels -= 1 # here for proper indexing
                self.adc_channels[self.num_channels].destroy_widget() # detroy tkinter widgets
                self.adc_channels.pop() # remove last item in list



# Functions
# whenever something needs to happen when changing the tabs
def update_tabs(event):
    nope = 0

# for serial spinbox to keep typed values in range
# don't know how it all works, grabbed from stackoverflow and changed some shit around
def correct_input(text):
    valid = False
    if text.isdigit():
        if (int(text) <= 127 and int(text) >= 1):
            valid = True
    elif text == '':
        valid = True
    return valid

# check that all is good and if so send settings to all systems
def input_validation():
    all_good = True
    
    # makes sure that all channels have channel, type, and serial selected
    for wanda in wanda_adc_channels.adc_channels:
        if wanda.entry_channel.get().strip() == '':
            messagebox.showwarning(title='Incomplete Input', message='You are missing a channel')
            all_good = False
        if wanda.entry_type.get().strip() == '':
            messagebox.showwarning(title='Incomplete Input', message='You are missing a type')
            all_good = False
        if wanda.entry_type_name.get().strip() == '':
            messagebox.showwarning(title='Incomplete Input', message='You are missing a type name')
            all_good = False
        if wanda.entry_unit.get().strip() == '':
            messagebox.showwarning(title='Incomplete Input', message='You are missing a unit')
            all_good = False
        if wanda.entry_serial.get().strip() == '':
            messagebox.showwarning(title='Incomplete Input', message='You are missing a serial')
            all_good = False
    
    # makes sure mode and rocket are selected
    if tv_entry_mode.get().strip() == '':
        messagebox.showwarning(title='Incomplete Input', message='You are missing the mode')
        all_good = False
    if tv_entry_rocket.get().strip() == '':
        messagebox.showwarning(title='Incomplete Input', message='You are missing the rocket')
        all_good = False
    
    # make sure there is a valid file name
    if config_log_name.get().strip() == '':
        messagebox.showwarning(title='Incomplete Input', message='You are missing the file name')
        all_good = False
    
    # log settings and send them if that are all good
    if all_good:
        log()
        stm32_send()
        tv.tv_send(wanda_adc_channels, tv_entry_mode, tv_entry_rocket)
        wanda_send()

# sending stm 32 data
def stm32_send():
    stm32_log = open(stm32_log_path, 'w')
    
    # loop through switches
    for switch in stm32_entry_switches:
        if switch.get().strip() == '':
            stm32_log.write('Empty\n')
        else:
            stm32_log.write(switch.get().strip()+'\n')
    # loop through buttons
    for button in stm32_entry_buttons:
        if button.get().strip() == '':
            stm32_log.write('Empty\n')
        else:
            stm32_log.write(button.get().strip()+'\n')
    
    # may not need these
    stm32_log.write(tv_entry_mode.get()+'\n')
    stm32_log.write(tv_entry_rocket.get()+'\n')

    stm32_log.close()
    
# Wanda communication
# send unsigned, 32-bit int over network
def send_int(number: int):
    wandaSocket.sendall(number.to_bytes(length=4, byteorder="little", signed=False))
    errorcode = wandaSocket.recv(32)
    print(f"Error code: {int.from_bytes(errorcode, byteorder='little', signed=False)}")

# create configuration command
def get_config_command(channel_number: int, sensor_type: int, serial_number: int) -> int:
    return ADD_SENSOR_COMMAND | channel_number | (sensor_type << 6) | (serial_number << 9)

def wanda_send():
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            print("channel: " + str(channel.entry_channel.current()-1))
            print("type: " + str(channel.entry_type.current()))
            print("serial: " + str(channel.entry_serial.get()))
            send_int(get_config_command(channel.entry_channel.current()-1,
                                        channel.entry_type.current(),
                                        int(channel.entry_serial.get())))
# ^ good job Joey!

# how we save data so we don't need to reinput stuff
def log():
    config_log = open(config_log_path+config_log_name.get().strip()+'.txt', 'w')
    
    # wanda
    config_log.write(str(wanda_adc_channels.num_channels)+'\n')
    for channel in wanda_adc_channels.adc_channels:
        config_log.write(channel.data_channel.get()+'\n')
        config_log.write(channel.data_type.get()+'\n')
        config_log.write(channel.data_type_name.get()+'\n')
        config_log.write(channel.data_unit.get()+'\n')
        config_log.write(channel.data_serial.get()+'\n')
        config_log.write(channel.color_code+'\n')
        
    # stm 32
    for switch in stm32_entry_switches:
        if switch.get().strip() == '':
            config_log.write('\n')
        else:
            config_log.write(switch.get().strip()+'\n')
    for button in stm32_entry_buttons:
        if button.get().strip() == '':
            config_log.write('\n')
        else:
            config_log.write(button.get().strip()+'\n')
    
    # tv
    config_log.write(tv_entry_mode.get()+'\n')
    config_log.write(tv_entry_rocket.get()+'\n')
    
    config_log.close()

# how we read in the data that we saved
def read():
    if os.path.isfile(config_log_path+config_log_name.get().strip()+'.txt'):
        config_log = open(config_log_path+config_log_name.get().strip()+'.txt', 'r')
    else:
        messagebox.showwarning(title='Invalid Input', message='That file name is unavalable')
        return
    
    # wanda
    loop = int(config_log.readline().strip())
    
    for i in range(loop):
        wanda_adc_channels.add_channel(1)
        wanda_adc_channels.adc_channels[i].data_channel.set(config_log.readline().strip())
        wanda_adc_channels.adc_channels[i].data_type.set(config_log.readline().strip())
        wanda_adc_channels.adc_channels[i].data_type_name.set(config_log.readline().strip())
        wanda_adc_channels.adc_channels[i].data_unit.set(config_log.readline().strip())
        wanda_adc_channels.adc_channels[i].data_serial.set(config_log.readline().strip())
        wanda_adc_channels.adc_channels[i].color_code = config_log.readline().strip()
        wanda_adc_channels.adc_channels[i].color_button.config(bg=wanda_adc_channels.adc_channels[i].color_code)
    wanda_adc_channels.delete_channel(1)
    
    # stm 32
    for switch in stm32_data_switches:
        switch.set(config_log.readline().strip())
    for button in stm32_data_buttons:
        button.set(config_log.readline().strip())
    
    # tv
    tv_data_mode.set(config_log.readline().strip())
    tv_data_rocket.set(config_log.readline().strip())
    
    config_log.close()



# Variables
padding = 5
stm32_log_path = 'Python Output/stm32_log.txt' # will need to update later
tv_log_path = 'Python Output/alldata.txt' # will need to update later
config_log_path = 'Python Output/' # will need to update later
prev_selection = 0

# Window and tab setup and control
# root
root = Tk()
root.title("KXR: LTI Configurations")
root.geometry("1200x600")
validate_input = (root.register(correct_input), '%P')

# font settings
normal_font = tkFont.Font(family='calibre', size=12, weight='normal')
bold_font = tkFont.Font(family='calibre', size=12, weight='bold')
root.option_add('*Font', bold_font)
root.option_add('*TCombobox*Font', normal_font)
root.option_add('*Spinbox*Font', normal_font)
root.option_add('*Entry*Font', normal_font)
root.option_add('*Button*Font', normal_font)

# tab creation
tabControl = ttk.Notebook(root)
wanda_tab = ttk.Frame(tabControl)
stm32_tab = ttk.Frame(tabControl)
tv_tab = ttk.Frame(tabControl)
confirm_tab = ttk.Frame(tabControl)

# tab settings
tabControl.bind('<<NotebookTabChanged>>', update_tabs)
tabControl.add(wanda_tab, text='Wanda')
tabControl.add(stm32_tab, text='STM 32')
tabControl.add(tv_tab, text='Telemetry Viewer')
tabControl.add(confirm_tab, text ='Confirmation')
tabControl.pack(fill="both", expand=1)



# !!!!!-----WANDA-----!!!!!

# How The Scrollbar Works (Please Do Not Touch)
# Create A Main Frame
wanda_mframe = Frame(wanda_tab)
wanda_mframe.pack(fill='both', expand=1)
# Create A Canvas
wanda_canvas = Canvas(wanda_mframe)
wanda_canvas.pack(side='left', fill='both', expand=1)
# Add A Scrollbar To The Canvas
wanda_scrollbar = ttk.Scrollbar(wanda_mframe, orient='vertical', command=wanda_canvas.yview)
wanda_scrollbar.pack(side='right', fill='y')
# Configure The Canvas
wanda_canvas.configure(yscrollcommand=wanda_scrollbar.set)
wanda_canvas.bind('<Configure>', lambda e: wanda_canvas.configure(scrollregion=wanda_canvas.bbox('all')))
# Create ANOTHER Frame INSIDE The Canvas
wanda_sframe = Frame(wanda_canvas)
# Add That New Frame To A Window In The Canvas
wanda_canvas.create_window((0,0), window=wanda_sframe, anchor='nw')
# End of Scrollbar Code

# Start of actually reading in user input (use: wanda_sframe)
Label(wanda_sframe, text ='Wanda Options:').grid(row=0, column=0, padx=padding, pady=padding)


# ADC CHANNELS
# just some labes for the channels
Label(wanda_sframe, text='[ADC]').grid(row=1, column=0, padx=padding, pady=padding)
Label(wanda_sframe, text='Physical').grid(row=3, column=0, padx=padding, pady=padding)
Label(wanda_sframe, text='Type').grid(row=3, column=1, padx=padding, pady=padding)
Label(wanda_sframe, text='Type Name').grid(row=3, column=2, padx=padding, pady=padding)
Label(wanda_sframe, text='Unit').grid(row=3, column=3, padx=padding, pady=padding)
Label(wanda_sframe, text='Serial').grid(row=3, column=4, padx=padding, pady=padding)

# values for the user to select
wanda_adc_channel_values = [' ', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'AUX1', 'AUX2', 'AUX3', 'AUX4']
wanda_adc_channel_checker = [] # user input validation
for i in range(41):
    wanda_adc_channel_checker.append(0)
wanda_adc_type_values = ['Pressure Transducer', 'Load Cell', 'Thermocouple']
wanda_adc_pressure_values = [' ', 'Rocket_Nitrogen', 'Rocket_Nitrogen_Regulated', 'Rocket_N2O', 'Rocket_Comb_Chamber', 'Rocket_Injector', 'Wanda_N2O', 'Wanda_Nitrogen', 'Wanda_Air']
wanda_adc_load_values = [' ', 'Load_Cell_1', 'Load_Cell_2', 'Load_Cell_3'] #Load_Cell_All for sending to tv
wanda_adc_thermo_values = [' ', 'Rocket_N2O_Vent', 'Rocket_N2O_Tank_Top', 'Rocket_N2O_Tank_Middle', 'Rocket_N2O_Tank_Bottom', 'Rocket_Comb_Chamber']
wanda_adc_unit_values = [' ', 'PSI', 'Pounds', 'Celsius', 'Fahrenheit']

# object used to hold all adc channels
wanda_adc_channels = adc_channel_list()

# used to select how many rows to create and delete
loop_count = Spinbox(wanda_sframe, from_=1, to=39, wrap=True)
loop_count.grid(row=2, column=0, padx=padding, pady=padding)
Button(wanda_sframe, text='Add', command=lambda: wanda_adc_channels.add_channel(int(loop_count.get()))).grid(row=2, column=1, padx=padding, pady=padding)
Button(wanda_sframe, text='Delete', command=lambda: wanda_adc_channels.delete_channel(int(loop_count.get()))).grid(row=2, column=2, padx=padding, pady=padding)

# just padding for scrollbar
for i in range(48):
    Label(wanda_sframe, text='').grid(row=i+4, column=0, padx=padding, pady=padding)
Label(wanda_sframe, text='You found me! :)').grid(row=52, column=0, padx=padding, pady=padding)

wanda_adc_channels.add_channel(int(loop_count.get())) # initialize first row



# !!!!!-----STM 32-----!!!!!

# How The Scrollbar Works (Please Do Not Touch)
# Create A Main Frame
stm32_mframe = Frame(stm32_tab)
stm32_mframe.pack(fill='both', expand=1)
# Create A Canvas
stm32_canvas = Canvas(stm32_mframe)
stm32_canvas.pack(side='left', fill='both', expand=1)
# Add A Scrollbar To The Canvas
stm32_scrollbar = ttk.Scrollbar(stm32_mframe, orient='vertical', command=stm32_canvas.yview)
stm32_scrollbar.pack(side='right', fill='y')
# Configure The Canvas
stm32_canvas.configure(yscrollcommand=stm32_scrollbar.set)
stm32_canvas.bind('<Configure>', lambda e: stm32_canvas.configure(scrollregion=stm32_canvas.bbox('all')))
# Create ANOTHER Frame INSIDE The Canvas
stm32_sframe = Frame(stm32_canvas)
# Add That New Frame To A Window In The Canvas
stm32_canvas.create_window((0,0), window=stm32_sframe, anchor='nw')
# End of Scrollbar Code

# Start of actually reading in user input (use: stm32_sframe)
Label(stm32_sframe, text ='STM 32 Options:').grid(row=0, column=0, padx=padding, pady=padding)


# SWITCHES
Label(stm32_sframe, text='[SWITCHES]').grid(row=1, column=0, padx=padding, pady=padding)
Label(stm32_sframe, text='Name').grid(row=1, column=1, padx=padding, pady=padding)

stm32_data_switches = []
stm32_entry_switches = []

for i in range(10):
    Label(stm32_sframe, text=f'Switch {i+1}').grid(row=i+2, column=0, padx=padding, pady=padding)
    stm32_data_switches.append(StringVar())
    stm32_entry_switches.append(Entry(stm32_sframe, textvariable=stm32_data_switches[i]))
    stm32_entry_switches[i].grid(row=i+2, column=1, padx=padding, pady=padding)

# BUTTONS
Label(stm32_sframe, text='').grid(row=13, column=0, padx=padding, pady=padding)
Label(stm32_sframe, text='[BUTTONS]').grid(row=14, column=0, padx=padding, pady=padding)
Label(stm32_sframe, text='Name').grid(row=14, column=1, padx=padding, pady=padding)

stm32_data_buttons = []
stm32_entry_buttons = []

for i in range(5):
    Label(stm32_sframe, text=f'Button {i+1}').grid(row=i+15, column=0, padx=padding, pady=padding)
    stm32_data_buttons.append(StringVar())
    stm32_entry_buttons.append(Entry(stm32_sframe, textvariable=stm32_data_buttons[i]))
    stm32_entry_buttons[i].grid(row=i+15, column=1, padx=padding, pady=padding)

Label(stm32_sframe, text='').grid(row=20, column=0, padx=padding, pady=padding) # just padding at end of window



# !!!!!-----TELEMETRY VIEWER-----!!!!!

# How The Scrollbar Works (Please Do Not Touch)
# Create A Main Frame
tv_mframe = Frame(tv_tab)
tv_mframe.pack(fill='both', expand=1)
# Create A Canvas
tv_canvas = Canvas(tv_mframe)
tv_canvas.pack(side='left', fill='both', expand=1)
# Add A Scrollbar To The Canvas
tv_scrollbar = ttk.Scrollbar(tv_mframe, orient='vertical', command=tv_canvas.yview)
tv_scrollbar.pack(side='right', fill='y')
# Configure The Canvas
tv_canvas.configure(yscrollcommand=tv_scrollbar.set)
tv_canvas.bind('<Configure>', lambda e: tv_canvas.configure(scrollregion=tv_canvas.bbox('all')))
# Create ANOTHER Frame INSIDE The Canvas
tv_sframe = Frame(tv_canvas)
# Add That New Frame To A Window In The Canvas
tv_canvas.create_window((0,0), window=tv_sframe, anchor='nw')
# End of Scrollbar Code

# Start of actually reading in user input (use: tv_sframe)
Label(tv_sframe, text ='Telemetry Viewer Options:', font=('calibre', 12, 'bold')).grid(row=0, column=0, padx=padding, pady=padding)


# MODE
Label(tv_sframe, text ='Mode').grid(row=1, column=0, padx=padding, pady=padding)

tv_values_mode = ['Static', 'Launch']
tv_data_mode = StringVar()
tv_entry_mode = ttk.Combobox(tv_sframe, values=tv_values_mode, state='readonly', textvariable=tv_data_mode)
tv_entry_mode.grid(row=1, column=1, padx=padding, pady=padding)

# ROCKET
Label(tv_sframe, text ='Rocket').grid(row=2, column=0, padx=padding, pady=padding)

tv_values_rocket = ['Liquid', 'Solid', 'Hybrid']
tv_data_rocket = StringVar()
tv_entry_rocket = ttk.Combobox(tv_sframe, values=tv_values_rocket, state='readonly', textvariable=tv_data_rocket)
tv_entry_rocket.grid(row=2, column=1, padx=padding, pady=padding)

# RELAYS
Label(tv_sframe, text ='[RELAYS]').grid(row=3, column=0, padx=padding, pady=padding)
tv_relays = []
for i in range(8):
    tv_relays.append('empty')
    Label(tv_sframe, text =f'Relay {i+1}').grid(row=i+4, column=0, padx=padding, pady=padding)
    Label(tv_sframe, text =tv_relays[i]).grid(row=i+4, column=1, padx=padding, pady=padding)

# SOLENOIDS
Label(tv_sframe, text ='[SOLENOIDS]').grid(row=12, column=0, padx=padding, pady=padding)
tv_solenoids = []
for i in range(8):
    tv_solenoids.append('empty')
    Label(tv_sframe, text =f'Solenoid {i+1}').grid(row=i+13, column=0, padx=padding, pady=padding)
    Label(tv_sframe, text =tv_relays[i]).grid(row=i+13, column=1, padx=padding, pady=padding)

# SERVOS
Label(tv_sframe, text ='[SERVOS]').grid(row=21, column=0, padx=padding, pady=padding)
tv_servos = []
for i in range(4):
    tv_servos.append('empty')
    Label(tv_sframe, text =f'Servo {i+1}').grid(row=i+22, column=0, padx=padding, pady=padding)
    Label(tv_sframe, text =tv_relays[i]).grid(row=i+22, column=1, padx=padding, pady=padding)

Label(tv_sframe, text='').grid(row=26, column=0, padx=padding, pady=padding) # just padding at end of window



# !!!!!-----CONFIRMATION-----!!!!!

# How The Scrollbar Works (Please Do Not Touch)
# Create A Main Frame
confirm_mframe = Frame(confirm_tab)
confirm_mframe.pack(fill='both', expand=1)
# Create A Canvas
confirm_canvas = Canvas(confirm_mframe)
confirm_canvas.pack(side='left', fill='both', expand=1)
# Add A Scrollbar To The Canvas
confirm_scrollbar = ttk.Scrollbar(confirm_mframe, orient='vertical', command=confirm_canvas.yview)
confirm_scrollbar.pack(side='right', fill='y')
# Configure The Canvas
confirm_canvas.configure(yscrollcommand=confirm_scrollbar.set)
confirm_canvas.bind('<Configure>', lambda e: confirm_canvas.configure(scrollregion=confirm_canvas.bbox('all')))
# Create ANOTHER Frame INSIDE The Canvas
confirm_sframe = Frame(confirm_canvas)
# Add That New Frame To A Window In The Canvas
confirm_canvas.create_window((0,0), window=confirm_sframe, anchor='nw')
# End of Scrollbar Code

# Start of actually reading in user input (use: confirm_sframe)
Label(confirm_sframe, text ='Please Provide Config Name').grid(row=0, column=0, padx=padding, pady=padding)
config_log_name = Entry(confirm_sframe)
config_log_name.grid(row=1, column=0, padx=padding, pady=padding) # send the data
Button(confirm_sframe, text='Commit Settings', command=input_validation).grid(row=2, column=0, padx=padding, pady=padding) # send the data
Button(confirm_sframe, text='Read Settings', command=read).grid(row=3, column=0, padx=padding, pady=padding) # read and apply last settings

# testing purposes
# remove before release
#Button(confirm_sframe, text='TCP CHECK', command=lambda: wanda_send()).grid(row=1, column=1, padx=padding, pady=padding)
#Button(confirm_sframe, text='PRINT SENSORS', command=lambda: send_int(0x55000000)).grid(row=2, column=1, padx=padding, pady=padding)
#Button(confirm_sframe, text='UWU 32', command=stm32_send).grid(row=3, column=1, padx=padding, pady=padding)
#Button(confirm_sframe, text='user', command=input_validation).grid(row=4, column=1, padx=padding, pady=padding)
#Button(confirm_sframe, text='color', command=tv_send).grid(row=5, column=1, padx=padding, pady=padding)

Label(confirm_sframe, text='').grid(row=4, column=0, padx=padding, pady=padding) # just padding at end of window



# END
root.mainloop()
#root.destroy()
