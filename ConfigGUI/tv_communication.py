from KXR_LTI_config_settings import wanda_adc_channels
from KXR_LTI_config_settings import tv_entry_mode
from KXR_LTI_config_settings import tv_entry_rocket


# sending tv data
def tv_send():
    print("mode: " + tv_entry_mode.get())
    print("rocket: " + tv_entry_rocket.get())
    
    # loop through adc channels
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            print("channel: " + str(channel.entry_channel.current()-1))
            print("type: " + str(channel.entry_type.current()))
            print("serial: " + str(channel.entry_serial.get()))
            print("color: " + str(channel.color_code))