import serial
import time
import joblib
import scipy
import numpy as np
import matplotlib
import pandas as pd
import sklearn
import math
import tensorflow as tf
import random
import itertools
import keyboard

from collections import Counter
from tensorflow.keras.utils import to_categorical
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from tensorflow.keras import layers, regularizers
from tensorflow.keras.models import Model

#%%
# Set up serial connection (adjust 'COM3' and baudrate as per your setup)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(1)  # Wait for connection to establish

#%%
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
def stop_script(event):
    if event.name == 'esc':  # Change 'esc' to the desired key
        print("Stopping the script and breaking serial connections...")
        ser.close()  # Close the serial connection
        exit()  # Exit the script
        
keyboard.on_press(stop_script)
#%%
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
#%%
model = joblib.load('crop_recommendation_Classification_1.joblib')
#%% Generate permutations for possible crops
def generate_permutations(numbers, adjustments):
      permutations = []
      for change in itertools.product([-1, 0, 1], repeat=len(numbers)):
          new_numbers = [number + (adjustment * c) for number, adjustment, c in zip(numbers, adjustments, change)]
          permutations.append(new_numbers)
      return permutations

# Adjustments
adjustments = [50, 50, 50, 50, 50, 50, 50, 50] # Change by 1 standard deviation
viable_crops = [] 
#%%
# Open a file to write

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        input_tuple = line.split(',')
        # Convert values to float, skipping empty strings
        try:
            input_tuple = [float(val) for val in input_tuple if val != '']
        except ValueError as e:
            print(f"Error converting to float: {e}")
            continue  # Skip this iteration and move on to the next line
        except KeyboardInterrupt:
        # Close the serial connection if Ctrl+C is pressed
            ser.close()
        
        print()  # For debugging purposes
        input = [float(x) for x in input_tuple]
        input_arduino = np.array(input)
        input_arduino = input_arduino[[4,5,6,1,0,3,2]]
        print(input_arduino)  # Optional: for real-time printing in the console
        #reorder the data
        input_pred = tf.convert_to_tensor(input_arduino.astype('float32'))
        input_pred_reshaped = np.reshape(input_pred, (1, -1))
        
        if keyboard.is_pressed("a"):
            predictions = model.predict(input_pred_reshaped)
            predictions_round = np.round(predictions)
            decoded_predictions = np.argmax(predictions_round, axis=1)
            decoded_predictions = encoder.inverse_transform(decoded_predictions)
            print(decoded_predictions)
            continue
        
        if keyboard.is_pressed("b"):
            permutations = np.array(generate_permutations(input_arduino, adjustments))
            # permutations_pred_reshaped = np.reshape(permutations, (len(permutations), -1))
            for i in range(len(permutations)):
                permutation = permutations[i,:]
                permutation = np.reshape(permutation,(1,-1))
                permutation_prediction = model.predict(permutation)  # Indexing to get a single sample
                permutation_prediction_round = np.round(permutation_prediction)
                decoded_permutation_prediction = np.argmax(permutation_prediction_round, axis=1)
                decoded_permutation_prediction = encoder.inverse_transform(decoded_permutation_prediction)
                viable_crops.append(decoded_permutation_prediction.tolist())
                
                crops_one_list = [item for sublist in viable_crops for item in sublist] # Change into one list
                word_counts = Counter(crops_one_list)
                unique_strings = list(word_counts.keys())
                # Get counts of unique strings
                counts = list(word_counts.values())
                # Print unique strings and their counts
                for string, count in zip(unique_strings, counts):
                    print(f"{string}: {count}")
                    
                
                
            
 
        
        
                            
