# GIP
This directory holds several scripts that were developed for the software side of teh digital twin protoype for my Group Industrial Project at University. This project involved designing a prototype digital twin to aid the automation of crop farming. The software side involved wireless connection between the back-end and the prototype, producing the back-end functions to control and send instructions, creating simple neural networks to predict ideal crops to grow from the grwoing conditions sensed from the prototype and connection to both Arduino Cloud and a simple front-end. There is also an example of the activation scripts written in Arduino to activate the nutrient distribution system.

The final main script is named DigitalTwinLayout which holds the functions and the connection to Arduino Cloud for the protoype to read. The machine learning scripts involve using the Crop Recommendation dataset, taken from Kaggle, and using different techniques to test different neural networks. Several statistical analysis was attempted by creating a artificial dataset to test the tangibility of unsupervised learning. To gather data for this dataset a heatmap analysis on reasearched weather data was conducted.

# Documentation: DigitalTwinLayout
## Overview
This project is designed to monitor and manage agricultural conditions using IoT devices connected to the Arduino Cloud. It collects real-time sensor data such as soil nutrients (N, P, K), temperature, humidity, pH levels, and rainfall, comparing them against ideal conditions to provide automatic recommendations and adjustments for optimized crop growth. Additionally, it uses a machine learning (ML) model to recommend the most suitable crops based on current environmental conditions.

## Features
- Sensor Data Collection:
  - Collects sensor data such as nutrient levels (N, P, K), temperature, humidity, rainfall, and pH.
  - Connects to Arduino Cloud to retrieve live sensor data.
- Automated Adjustments:
  - Automatic actuation of servos for water irrigation, nutrient mixing, and protection against excessive rainfall (parasol mechanism).
  - Compares current sensor values against predefined ideal values and triggers corresponding actuators to maintain optimal growing conditions.
- Machine Learning Crop Recommendation:
  - Recommends viable crops based on current environmental data using a pre-trained machine learning model.
  - Provides crop recommendations with permutation analysis to simulate possible changes in conditions and suggest the best possible crops.
- Farmer Interactions:
  - Allows manual farmer interaction through the Arduino Cloud interface for control over irrigation systems and parasol mechanisms.

## Code Structure
Libraries Used
- NumPy: For array and numerical operations.
- Pandas: For data manipulation and analysis.
- TensorFlow: For running machine learning models to predict viable crops.
- ArduinoCloudClient: To connect and communicate with the Arduino Cloud.
- Logging: For generating detailed runtime logs.
- Nest Asyncio: To handle asynchronous operations.
- Custom Functions: Located in classification_function_file, used for crop prediction.
  
## Main Functions
1. compare_values():
Compares the real-time sensor data (e.g., N, P, K) against ideal values and activates the servo motors for appropriate action (e.g., irrigation or nutrient dispersion).
2. compare_pH():
Similar to compare_values(), but specifically adjusts pH levels by activating servos to dispense high or low pH solutions.
3. n_time_fun(), p_time_fun(), k_time_fun(), etc.:
Calculate the time for which the servo motor should be activated based on the difference between current and ideal values for specific environmental factors (N, P, K, temperature, humidity, pH, rainfall).
4. ideal_crop_recommendation():
Uses current environmental data to predict suitable crops based on a pre-trained machine learning model.
5. permutation_ideal_crop_recommendation():
Performs permutations of the environmental data to simulate changes and predict the most viable crops in various possible conditions.
7. Manual Controls:
Functions like check_temp(), fake_function(), and JS_switch() allow manual testing and control of the system, such as toggling parasol expansion or setting test temperature values.

## IoT Communication Setup
Arduino Cloud Client Configuration
Uses Device ID and Secret Key to connect to Arduino Cloud
The project connects to the Arduino Cloud using the ArduinoCloudClient class, which handles all the registered variables and their respective functions for data processing and actuation.

## Running the Project
- Prerequisites
  - Arduino Cloud account with device set up.
  - Python libraries installed (NumPy, Pandas, TensorFlow).
  - Classification model and custom functions file (located in classification_function_file).
## Execution Steps
- Set up the Arduino Cloud environment and ensure the correct device ID and secret key are configured.
- Install necessary dependencies (numpy, pandas, tensorflow, etc.).
- Run the script to start data collection and processing:
- Monitor real-time sensor values and allow the system to make adjustments or manually trigger functions via the Arduino Cloud dashboard.
## Future Improvements
- Expand crop recommendation capabilities with additional environmental factors and use primary collected data to produce continuous learning models
- Integrate more advanced machine learning models to improve accuracy in crop predictions.
- Implement a web-based dashboard for easier farmer interaction.
