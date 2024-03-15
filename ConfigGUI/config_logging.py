from tkinter import messagebox
import os

# how we save data so we don't need to reinput stuff
def log(config_log_path, config_log_name, wanda_adc_channels, stm32_entry_switches, stm32_entry_buttons, tv_entry_mode, tv_entry_rocket):
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
        
    # stm32
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
def read(config_log_path, config_log_name, wanda_adc_channels, stm32_data_switches, stm32_data_buttons, tv_data_mode, tv_data_rocket):
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
    
    # stm32
    for switch in stm32_data_switches:
        switch.set(config_log.readline().strip())
    for button in stm32_data_buttons:
        button.set(config_log.readline().strip())
    
    # tv
    tv_data_mode.set(config_log.readline().strip())
    tv_data_rocket.set(config_log.readline().strip())
    
    config_log.close()
