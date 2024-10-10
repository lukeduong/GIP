import numpy as np
import math 
import pandas as pd
import random
import keyboard
import serial
import time
import joblib
import tensorflow as tf
import sklearn
import itertools
from tensorflow.keras import layers, regularizers
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
# regression + continuous learning --> ideal parameters
# regression --> prediction of near future parameters for thatg controlled environement
# compare prediction and current parameters to the ideal parameters
# too low or too big --> activation of some sort

#%% Ideal Values for Parameters from Regression Learning Code
N_ideal = 35
P_ideal = 130
K_ideal = 290
temp_ideal = 22 
humidity_ideal = 95 
pH_ideal = 6
rainfall_ideal = 110

ideal_parameters = np.array([N_ideal, P_ideal, K_ideal, temp_ideal, humidity_ideal, pH_ideal, rainfall_ideal])

#%% dont actually need this in final code
size = 100000
# rainfall dist
rain_mean = 200
rain_sd = 50
rain_norm_dist = np.random.normal(rain_mean,rain_sd,size)
# temperature dist
temperature_mean = 24
temperature_sd = 2.5
temperature_norm_dist = np.random.normal(temperature_mean, temperature_sd, size)
# pH dist
pH_mean = 5.5
pH_sd = 0.5
pH_norm_dist = np.random.normal(pH_mean, pH_sd, size)
# humidity dist
humidity_mean = 50
humidity_sd = 10
humidity_norm_dist = np.random.normal(humidity_mean, humidity_sd, size)
# Nitrogen dist
N_mean = 25
N_sd = 5
N_norm_dist = np.random.normal(N_mean, N_sd, size)
# Phosphorous dist
P_mean = 130
P_sd = 10
P_norm_dist = np.random.normal(P_mean, P_sd, size)
# Potassium dist
K_mean = 200
K_sd = 5
K_norm_dist = np.random.normal(K_mean, K_sd, size)

def random_current_values(rain_norm_dist, temperature_norm_dist, pH_norm_dist, humidity_norm_dist, N_norm_dist, P_norm_dist, K_norm_dist):
     rain_random_value = np.random.choice(rain_norm_dist)
     temperature_random_value = np.random.choice(temperature_norm_dist)
     pH_random_value = np.random.choice(pH_norm_dist)
     humidity_random_value = np.random.choice(humidity_norm_dist)
     N_random_value = np.random.choice(N_norm_dist)
     P_random_value = np.random.choice(P_norm_dist)
     K_random_value = np.random.choice(K_norm_dist)
     current_parameters_def = np.array([N_random_value, P_random_value, K_random_value, temperature_random_value, humidity_random_value, pH_random_value, rain_random_value], 'float32')
     return current_parameters_def
 
#%% Prediction of future parameters
# 
#%% Classification (IDEAL CROP)
# Call up the CLassification model
@tf.keras.utils.register_keras_serializable()
class FCNN(Model):
    def __init__(self):
        super(FCNN, self).__init__()
        self.fcnn = tf.keras.Sequential([
            layers.Dense(7, input_shape=(7,), activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(22, activation='softmax')  # Adjusted output size for multiclass classification
        ])

    def call(self, x):
        output = self.fcnn(x)
        return output

def DefModel():
    return FCNN()
model = joblib.load('crop_recommendation_Classification_1.joblib')

csv_file_path = 'C:/Users/luked/OneDrive/Desktop/Year 4/GIP/GIP/Crop_recommendation.csv'
crop_data = pd.read_csv(csv_file_path)

crop_data = pd.DataFrame(data = crop_data)
crop_data_df = crop_data.copy()
crop_data_df.iloc[:, :7] = (crop_data_df.iloc[:, :7] - crop_data_df.iloc[:, :7].min()) / (crop_data_df.iloc[:, :7].max() - crop_data_df.iloc[:, :7].min())

# Shuffle data
crop_data_df_shuffled = np.random.permutation(crop_data_df)

x_data = crop_data_df_shuffled[:,0:7]
y_data = crop_data_df_shuffled[:,7]
encoder = LabelEncoder()
encoder.fit(y_data)
encoded_y = encoder.transform(y_data)
dummy_y = to_categorical(encoded_y)


x_data = tf.convert_to_tensor(x_data.astype('float32'))
y_data = tf.convert_to_tensor(dummy_y)

#%%
# Generate Permutations
def generate_permutations(numbers, adjustments):
      permutations = []
      for change in itertools.product([-1, 0, 1], repeat=len(numbers)):
          new_numbers = [number + (adjustment * c) for number, adjustment, c in zip(numbers, adjustments, change)]
          permutations.append(new_numbers)
      return permutations
# Adjustments
adjustments = [5, 10, 3, 8, 12, 6, 9, 15] # Change by 1 standard deviation 

while True:
    if keyboard.is_pressed("a"):
        input_arduino = random_current_values(rain_norm_dist, temperature_norm_dist, pH_norm_dist, humidity_norm_dist, N_norm_dist, P_norm_dist, K_norm_dist)
        time.sleep(0.1)
        print("Random current values:", input_arduino)

        # Compare against Ideal Parameters
        comparison_sensor = ideal_parameters - input_arduino
        comparison_sensor = np.round(comparison_sensor)
        time.sleep(5) # every 1 
        print("Difference from Ideal:", comparison_sensor)
        
        # Recommend ideal crop
        input_pred_reshaped = np.reshape(input_arduino, (1, -1))
        input_pred = tf.convert_to_tensor(input_pred_reshaped.astype('float32'))
        
        predictions = model.predict(input_pred)
        predictions_round = np.round(predictions)
        decoded_predictions = np.argmax(predictions_round, axis=1)
        decoded_predictions = encoder.inverse_transform(decoded_predictions)
        print(decoded_predictions)
        
        # Find 
        

        # Generate permutations
        permutations = generate_permutations(input_arduino, adjustments)

    
    # Compare the Near Future Predicted 
    # comparison_predicted = ideal_parameters 
    
    
    
# Current Values for the Parameters
# in the while True loop
# input_arudino = []
# current_parameters = np.copy(input_arudino)

# Future predicted values for the Parameters
