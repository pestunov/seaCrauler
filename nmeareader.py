import serial
import time
import re
import pandas as pd
import numpy as np

def coord_convert(num) -> float:
    num = float(num)/100
    res = num - int(num)
    return int(num) + res / 60 * 100


df = pd.DataFrame(columns=['source', 'lat', 'long'])
counter = 50000

with serial.Serial('/dev/ttyUSB0', '4800', timeout=0) as ser:
    buf_str = ''
    while(counter > 0):
        read_data = str(ser.read(10000)).upper()
        if len(read_data) >= 3:
            buf_str += read_data[2:-1]
        data = re.split(r'\\N', buf_str)
        buf_str = ''
        for i in data:
            counter -= 1
            if not re.search(r'\\R$', i):
                buf_str = i
                break
            if re.match(r'\$GNGLL', i):
                data_list = re.split(',', i)
                lat = coord_convert(data_list[1])
                long = coord_convert(data_list[3])
                print(f"GNGLL: lat = {lat}, long = {long}")
                df = df.append({'source': 'GNGLL', 'lat': lat, 'long': long}, ignore_index=True)
                continue

            if re.match(r'\$GNRMC', i):
                data_list = re.split(',', i)
                lat = coord_convert(data_list[3])
                long = coord_convert(data_list[5])
                print(f"GNRMC: lat = {lat}, long = {long}")
                df = df.append({'source': 'GNRMC', 'lat': lat, 'long': long}, ignore_index=True)
                continue

            if re.match(r'\$GPGGA', i):
                data_list = re.split(',', i)
                lat = coord_convert(data_list[2])
                long = coord_convert(data_list[4])
                df = df.append({'source': 'GPGGA', 'lat': lat, 'long': long}, ignore_index=True)
                print(f"GPGGA: lat = {lat}, long = {long}")
                continue
                
            else:
                print(f"not match")
        time.sleep(1)
        print(f"counter = {counter}")

df.to_csv('gps_data')       
        

