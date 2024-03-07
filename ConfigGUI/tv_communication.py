from KXR_LTI_config_settings import wanda_adc_channels
from KXR_LTI_config_settings import tv_entry_mode
from KXR_LTI_config_settings import tv_entry_rocket

tv_log_path = 'Python Output/alldata.txt' # will need to update later

# sending tv data
def tv_send():
    tv_log = open(tv_log_path, 'w')
    
    tv_log.write('Telemetry Viewer v0.8 Settings\n\
                 \n\
                 GUI Settings:\n\
                 \n\
                 tile column count = 6\n\
                 tile row count = 6\n\
                 time format = Only Time\n\
                 show 24-hour time = false\n\
                 show hint notifications = true\n\
                 hint notifications color = 0x00FF00\n\
                 show warning notifications = true\n\
                 warning notifications color = 0xFFFF00\n\
                 show failure notifications = true\n\
                 failure notifications color = 0xFF0000\n\
                 show verbose notifications = false\n\
                 verbose notifications color = 0x00FFFF\n\
                 show plot tooltips = true\n\
                 smooth scrolling = true\n\
                 show fps and period = false\n\
                 benchmarking = false\n\
                 antialiasing level = 8\n\
                 \n\
                 1 Connections:\n\
                 \n')
    
    # loop through adc channels
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            print('dataset location = ' + str( (channel.entry_channel.current()-1) * 4 + 1 ))
            print('binary processor = float32 LSB First')
            print('name = ' + str(channel.data_type_name.get()))
            print('color = 0x' + str(channel.color_code.replace('#', '')))
            print('unit = ' )
            print('conversion factor a = 1.0\n')
            print('conversion factor b = 1.0\n')
            print('\n')
    
    tv_log.write('checksum location = -1\n\
                 checksum processor = null\n\
                 \n\
                 0 Charts:\n\
                 \n')
    
    tv_log.write(tv_entry_mode.get()+'\n')
    tv_log.write(tv_entry_rocket.get()+'\n')

    tv_log.close()
