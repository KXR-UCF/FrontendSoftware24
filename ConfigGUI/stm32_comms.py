# sending stm32 data
def stm32_send(stm32_log_path, stm32_entry_switches, stm32_entry_buttons):
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
    #stm32_log.write(tv_entry_mode.get()+'\n')
    #stm32_log.write(tv_entry_rocket.get()+'\n')

    stm32_log.close()
