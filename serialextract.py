# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

import serial
import time

# Set up serial connection (adjust accordingly)
ser = serial.Serial('COM9', 9600, timeout=1)
time.sleep(1)  # Wait for connection to establish

while True:
    if ser.in_waiting > 0:
        # Read the line of data
        line = ser.readline().decode('utf-8').rstrip()
        
        # Split the line by commas to get individual values
        values = line.split(',')
        
        # Convert values to float, skipping empty strings
        try:
            values = [float(val) for val in values if val != '']
        except ValueError as e:
            print(f"Error converting to float: {e}")
            continue  # Skip this iteration and move on to the next line
        
        print(values)  # For debugging purposes
        

        # Convert list to a NumPy array
        my_array = np.array(values)
