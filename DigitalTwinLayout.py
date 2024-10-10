## DIGITAL TWIN
# Define Objectives: Clearly outline the objectives of the digital twin. Determine what specific aspects of the grapevine and grapes you want to simulate and monitor.
# Displays the current growing conditions

# Displays the current possible crops that can be grown in this condition (IDEAL CROP CLASSIFICATION MODEL)
# Displays the possible crops that can be grown with slight adjustments to the parameters (IDEAL CROP CLASSIFICATION MODEL)

# Calculates the ideal values for the growing conditions of the selected crop after historical usage
# *THIS IS DONE WITH A CONTINUOUS/REINFORCEMENT LEARNING MODEL WITH SYNTHETIC DATA*

# Displays what stage the plant is at (Need a time tracker and need a part an input to say what stage the plant is at)
# Displays growth of the plant
# Growth(N, P, K, Soil Temp, Soil Humidity, Conductivity, pH, light UV index, Temperature, Humidity, DateTime)
# Growth needs to be shown as a function of some parameters that we can sense or control
    # Need a model that learns the relationship between all/some of these parameters
    # Then predicts the current growth stage of the crop
    
#%% Add all the libraries
import numpy as np
import pandas as pd
import time 
import logging
import sys
import nest_asyncio
import random
import classification_function_file
import tensorflow as tf
sys.path.append("lib")
from arduino_iot_cloud import ArduinoCloudClient
from collections import Counter
#%% Gather Data: Collect relevant data from various sources such as sensors, historical records, and environmental databases. This data may include information on weather patterns, soil composition, grapevine characteristics, and past harvests.
    # Gather data from sensor
    # IOT connection get data from the Arduino Cloud
        # Connect to Arduino Cloud (DeviceID + Secret Key) Test
nest_asyncio.apply()
DEVICE_ID = "7a161377-56b4-4dac-8950-6da20458660f"
SECRET_KEY = "#QyP#Hf02KTFu2uCQq7LP!TRO"
def logging_func():
    logging.basicConfig(datefmt="%H:%M:%S",
                        format="%(asctime)s.%(msecs)03d %(message)s",
                        level=logging.INFO,)
    
    
    
# Functions
# Response and Activation: Using the model calculate the correct adjustments or predictions and call respective functions accodringly
    # Create DEF FUNCTIONS that do the correct adjustments suggested from the model
    # Water --> standard water irrigation system function
    # Too much rainfall --> open umbrella function
    # Nutrients or pH --> Mixture irrigation system
    # Allow for farmer manual interaction e.g. farmer can activate the umbrella mechanism
    
ideal_values = np.array([100,100,100,100,100,100,100])      # Ideal Growing conditions (N, P, K, Temperature, Humidity, Rainfall)#
# Comparing incoming sensor data to the ideal values
def compare_values(client, value, ideal_value, switch_variable, duration_variable, threshold, time_function, servo_number):
    diff =  ideal_value - value
    if diff > threshold:
        client[switch_variable] = True
        client[duration_variable] = time_function(diff)
        print("----------------------------------------------------")
        print(f"NDS Servo Pin: {servo_number}")
        print("Switch:", client[switch_variable])
        print("Duration the Servo is on for (milliseconds):", client[duration_variable])
        print(f"Actuation  -->   Value:{value}    Difference:{diff}     Threshold:{threshold}")
    else:
        print("----------------------------------------------------")
        client[switch_variable] = False
        print("Switch:", client[switch_variable])
        print(f"No Actuation  -->  Value:{value}    Difference:{diff}     Threshold:{threshold}")

# Comparing the pH and adjusing with HIGH pH solution and LOW pH solution
def compare_pH(client, value, ideal_value, switch_variable, duration_variable, threshold, time_function, servo_number):
    diff = ideal_value - value
    if diff > threshold:
        print(diff)
        # here turn on certain servo to go back to correct pH
        # Also calc time that the servo must be turned on for
    if diff < threshold:
        print(diff)
        # here turn on certain servo to go back to correct pH
        # Also calc time that the servo must be turned on for
    else:
        # Dont do anything
        print("do nothing")

# Function to see if the parasol needs to be opened (Comparing Sunlight and Rainfall levels)
# def parasol_mechanism():
    
# Here define all the methods of calculating time(milliseconds) for the servo, with respect
# to the nutrient the servo is dispensing.
# N Time Function
def n_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# P Time Function
def p_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

#  Time Function
def k_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# Temperature Time Function
def temp_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# Humidity Time Function
def humid_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# pH Time Function
def ph_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# Rainfall Time Function
def rain_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# Light Time Funtion
def light_time_fun(diff):
    time_ms = int((diff*1000)/2.5)
    return time_ms

# ML Crop Recommendation Functions
def ideal_crop_recommendation(client, value):
    if value:
        n = int(client["n"])
        p = int(client["p"])
        k = int(client["k"])
        temp = int(client["temperature"])
        humid = int(client["humidity"])
        ph = int(client["pH"])
        rainfall = int(client["rainfall"])
        data = np.array([n,p,k,temp,humid,ph,rainfall])
        print(data)
        input_pred = tf.convert_to_tensor(data.astype('float32'))
        input_pred_reshaped = np.reshape(input_pred, (1, -1))
        viable_crops = np.array(classification_function_file.predict_idealcrops(input_pred_reshaped))
        print("Viable Crop:", viable_crops)

adjustments = [50, 50, 50, 50, 50, 50, 50, 50]
def permutation_ideal_crop_recommendation(client, value):
    if value:
        n = int(client["n"])
        p = int(client["p"])
        k = int(client["k"])
        temp = int(client["temperature"])
        humid = int(client["humidity"])
        ph = int(client["pH"])
        rainfall = int(client["rainfall"])
        data = np.array([n,p,k,temp,humid,ph,rainfall])
        permutations = classification_function_file.generate_permutations(data, adjustments)
        viable_crops = []
        for i in range(len(permutations)):
            permutation = permutations[i]
            permutation = np.reshape(permutation,(1,-1))
            permutation_prediction = classification_function_file.predict_idealcrops(permutation)
            # print(permutation_prediction)
            viable_crops.append(permutation_prediction.tolist())
            crops_one_list = [item for sublist in viable_crops for item in sublist] # Change into one list
            word_counts = Counter(crops_one_list)
            unique_strings = list(word_counts.keys())
            # Get counts of unique strings
            counts = list(word_counts.values())
            # Print unique strings and their counts
            for string, count in zip(unique_strings, counts):
                print(f"{string}: {count}")

# Testing JavaScript Buttons
def JS_switch(client, value):
    if value:
        print("This switch is on True")
        time.sleep(5)
        client["jS_Test"] = False
        print("Switch turned oFF")

def check_temp(client, value):
    # diff =  21 - value
    # if diff < -2:
    #     client["parasolExpand"] = True
    #     client["parasol_status"] = "Parasol is UP"
    #     client["parasolCollapse"] = False
    # if diff >= -2:
    #     client["parasolExpand"] = True
    #     client["parasolCollapse"] = True

    if value >= 18:
        client["parasolExpand"] = True
        client["parasol_status"] = "Parasol is UP"
        client["parasolCollapse"] = False
        client["servo_pin_2"] = True
    if value < 18:
        client["parasolExpand"] = True
        client["parasolCollapse"] = True
        
def fake_function(client, value):
    if value:
        temp = int(client["fake_temp"])
        if temp == 15:
            client["fake_temp"] = 16
            print(client["fake_temp"])
        if temp == 16:
            client["fake_temp"] = 18
            print(value)
        if temp == 18:
            client["fake_temp"] = 19
            print(value)
        if temp == 19:
            client["fake_temp"] = 21
            client["switch_fake"] = True
            print(value)
    else:
        print(value)
  
# Gather necessary data PREDICTION NEAR FUTURE MODEL
# Data Preprocessing: Clean and preprocess the collected data to ensure consistency and compatibility. This may involve handling missing values, normalizing data, and converting formats as necessary.
    # Adjust the units to the correct units for all the models
if __name__ == "__main__":
    logging_func()
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    ## Register all the Arduino Cloud variables and their respective functions
    # Arduino Sensor values
    # All in one sensor:

    client.register("n", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[0], "servo_pin_2", "servo2_duration", 1, lambda diff: n_time_fun(diff), 2))
    client.register("p", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[1], "servo_pin_3", "servo3_duration", 1, lambda diff: p_time_fun(diff), 3))
    client.register("k", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[2], "servo_pin_4", "servo4_duration", 1, lambda diff: k_time_fun(diff), 4))
    client.register("temperature", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[3], "servo_pin_5", "servo5_duration", 1, lambda diff: temp_time_fun(diff), 5))
    client.register("humidity", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[4], "servo_pin_6", "servo6_duration", 1, lambda diff: humid_time_fun(diff), 6))
    client.register("pH", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[5], "servo_pin_2", "servo2_duration", 1, lambda diff: ph_time_fun(diff), 2))
    client.register("rainfall", value=None, on_write=lambda client, value:compare_values(client, value, ideal_values[6], "servo_pin_3", "servo3_duration", 1, lambda diff: rain_time_fun(diff), 3))
    
    # Individual sensors
    # client.register("room_ALS", value=None, on_write=display_sensor_values, interval = 5.0)
    # client.register("room_humid", value=None, on_write=display_sensor_values, interval = 5.0)
    # client.register("room_ir", value=None, on_write=display_sensor_values, interval = 5.0)
    client.register("room_temp", value=None, on_write=check_temp, interval = 5.0)
    # client.register("room_uv", value=None, on_write=display_sensor_values, interval = 5.0)
    # client.register("room_UVS", value=None, on_write=display_sensor_values, interval = 5.0)
    # client.register("room_vis", value=None, on_write=display_sensor_values, interval = 5.0)
    
    # New Sensors
    client.register("parasolExpand",value=None)
    client.register("parasolCollapse",value=None)
    client.register("parasol_status", value=None)
    
    
    
    # Turn on/off the ideal crop recommendation
    client.register("ideal_crop_switch", on_write=ideal_crop_recommendation)    # Ideal crop recommendation (sensor)
    client.register("permutations_ideal_crop_switch", on_write=permutation_ideal_crop_recommendation)    # Ideal crop recommendation (permutations)
    # Turn on/off the Nutrient Distribution System (NDS)
    client.register("servo_pin_2")
    client.register("servo_pin_3")
    client.register("servo_pin_4")
    client.register("servo_pin_5")
    client.register("servo_pin_6")
    client.register("servo2_duration", value=None)
    client.register("servo3_duration", value=None)
    client.register("servo4_duration", value=None)
    client.register("servo5_duration", value=None)
    client.register("servo6_duration", value=None)
    
    # JavaScript Variables:
    client.register("jS_Test", on_write=ideal_crop_recommendation)
    
    
    # faking
    client.register("control_fake", on_write=fake_function)
    client.register("fake_temp", value=None)
    client.register("switch_fake", value=None)
    
    client.start()
    
      
#%% Data Integration: The digital twin collects and integrates data on various environmental factors (temperature, rainfall, soil moisture, etc.), grapevine characteristics, and historical data. This data forms the basis for decision-making.
    # Usage OF the PREDICTION NEAR FUTURE MODEL 
    # Analyse which parameters might be needing a change when compared to the cont inuous ideal values
#%% Model Development: Develop models to simulate the growth and behavior of the grapevine and grapes. This could involve creating mathematical models based on biological principles, empirical models derived from historical data, or machine learning algorithms trained on observational data.
    # Build functions that show the growth of the plant
    # Build functions that show the quality of the "fruit"
#%% Modeling: The digital twin incorporates models to simulate the growth and behavior of grapevines. These models can be expanded to include more sophisticated representations of vine physiology, pest and disease dynamics, nutrient uptake, and other relevant processes.
    # Show the nutriction uptake
    # Show the water uptake
    # Show the environment the crop is experiencing
#%% Integration: Integrate the developed models with the collected data to create a unified digital twin system. Ensure that the models can interact with each other and update dynamically based on real-time data inputs.
    # Usage of the respective models with the incoming sensor data
#%% Visualization: Develop visualization components to represent the digital twin's output in a user-friendly manner. This could include interactive dashboards, 3D visualizations of the grapevine, and graphs showing key metrics such as grape yield and quality over time.
    # Send tbe incoming sensor data to frontend application
    # Show the predicted data in frontend application
    # Very simple visulaisation/representation of the stage of the crop 
    # Show the possible human interactions with the digital twin actiavtion side
    # Show the heatmap of the different sensor data from the different umbrellas

#%% Feedback Loop: The DSS should incorporate feedback mechanisms to continuously improve its recommendations. This could involve collecting data on the outcomes of management decisions (e.g., yield, grape quality) and using this information to refine the underlying models and algorithms.
    # Collect the data on yield and quality from the farmer on the frontend side
    # Refine the continuous learning model accordingly 













