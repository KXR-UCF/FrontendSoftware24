import socket

# wanda info
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

# sending wanda data
# send unsigned, 32-bit int over network
def send_int(number: int):
    wandaSocket.sendall(number.to_bytes(length=4, byteorder="little", signed=False))
    errorcode = wandaSocket.recv(32)
    print(f"Error code: {int.from_bytes(errorcode, byteorder='little', signed=False)}")

# create configuration command
def get_config_command(channel_number: int, sensor_type: int, serial_number: int) -> int:
    return ADD_SENSOR_COMMAND | channel_number | (sensor_type << 6) | (serial_number << 9)

def wanda_send(wanda_adc_channels):
    temp = 0
    isLoadCell = False
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            if channel.entry_channel.current() > temp:
                temp = channel.entry_channel.current()
            if channel.data_type.get() == 'Load Cell':
                isLoadCell = True
            #print("channel: " + str(channel.entry_channel.current()-1))
            #print("type: " + str(channel.entry_type.current()))
            #print("serial: " + str(channel.entry_serial.get()))
            send_int(get_config_command(channel.entry_channel.current()-1,
                                        channel.entry_type.current(),
                                        int(channel.entry_serial.get())))
    if isLoadCell:
        send_int(get_config_command(temp, 1, 0))
# ^ good job Joey!