tv_log_path = 'Python Output/alldata.txt' # will need to update later


def tv_send(wanda_adc_channels, tv_entry_mode, tv_entry_rocket):
    tv_log = open(tv_log_path, 'w')
    
    temp = 0
    isLoadCell = False
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            if channel.entry_channel.current() > temp:
                temp = channel.entry_channel.current()
            if channel.data_type.get() == 'Load Cell':
                isLoadCell = True
    
    tv_log.write('Telemetry Viewer v0.8 Settings\n\
\n\
GUI Settings:\n\
\n\
\ttile column count = 6\n\
\ttile row count = 6\n\
\ttime format = Only Time\n\
\tshow 24-hour time = false\n\
\tshow hint notifications = true\n\
\thint notifications color = 0x00FF00\n\
\tshow warning notifications = true\n\
\twarning notifications color = 0xFFFF00\n\
\tshow failure notifications = true\n\
\tfailure notifications color = 0xFF0000\n\
\tshow verbose notifications = false\n\
\tverbose notifications color = 0x00FFFF\n\
\tshow plot tooltips = true\n\
\tsmooth scrolling = true\n\
\tshow fps and period = false\n\
\tbenchmarking = false\n\
\tantialiasing level = 8\n\
\n\
1 Connections:\n\
\n\
\tconnection type = UDP\n\
\tserver port = 8080\n\
\tpacket type = Binary\n\
\tsample rate hz = 24\n\
\tsync word = 0xAA\n\
\tsync word byte count = 1\n\
')
    if isLoadCell:
        tv_log.write('\tdatasets count = ' + str(wanda_adc_channels.num_channels + 1) + '\n\n')
    else:
        tv_log.write('\tdatasets count = ' + str(wanda_adc_channels.num_channels) + '\n\n')
    
    # loop through adc channels
    for channel in wanda_adc_channels.adc_channels:
        if channel.entry_channel.current() != 0:
            tv_log.write('\t\tdataset location = ' + str( (channel.entry_channel.current()-1) * 4 + 1 ) + '\n')
            tv_log.write('\t\tbinary processor = float32 LSB First\n')
            tv_log.write('\t\tname = ' + str(channel.data_type_name.get()) + '\n')
            tv_log.write('\t\tcolor = 0x' + str(channel.color_code.replace('#', '')) + '\n')
            tv_log.write('\t\tunit = ' + str(channel.data_unit.get()) + '\n')
            tv_log.write('\t\tconversion factor a = 1.0\n')
            tv_log.write('\t\tconversion factor b = 1.0\n')
            tv_log.write('\n')
        
    if isLoadCell:
        tv_log.write('\t\tdataset location = ' + str( (temp) * 4 + 1 ) + '\n')
        tv_log.write('\t\tbinary processor = float32 LSB First\n')
        tv_log.write('\t\tname = Load_Cell_all\n')
        tv_log.write('\t\tcolor = 0x000000\n')
        tv_log.write('\t\tunit = Pounds\n')
        tv_log.write('\t\tconversion factor a = 1.0\n')
        tv_log.write('\t\tconversion factor b = 1.0\n')
        tv_log.write('\n')
    
    tv_log.write('\t\tchecksum location = -1\n\
\t\tchecksum processor = null\n\
\n\
0 Charts:\n\
\n')
    
    #tv_log.write(tv_entry_mode.get()+'\n')
    #tv_log.write(tv_entry_rocket.get()+'\n')

    tv_log.close()
