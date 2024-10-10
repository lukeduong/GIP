# Classification Function File
import numpy as np
import itertools
import tensorflow as tf
import joblib
import pandas as pd
from tensorflow.keras import layers, regularizers
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from collections import Counter

#%% Retrieve Classification Model
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
#%% Retrieve Encoder
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

#%% Creating functions
# Generate the permutations
def predict_idealcrops(input_data):
    ideal_crop_prediction = model.predict(input_data)
    # return ideal_crop_prediction
    decoded_predictions = np.argmax(ideal_crop_prediction, axis=1)
    decoded_predictions = encoder.inverse_transform(decoded_predictions)
    return decoded_predictions
    # decoded_prediction = encoder.inverse_transform(ideal_crop_prediction)
    # return decoded_prediction


def generate_permutations(numbers, adjustments):
      permutations = []
      for change in itertools.product([-1, 0, 1], repeat=len(numbers)):
          new_numbers = [number + (adjustment * c) for number, adjustment, c in zip(numbers, adjustments, change)]
          permutations.append(new_numbers)
      return permutations
      
# Decode
def decode(values):
    decoded_prediction = encoder.inverse_transform(values)
    return decoded_prediction


# Predict the ideal crops for all permutations
def predict_idealcrops_permutations(permutations):
    viable_crops = []
    viable_crop_count = []
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
            viable_crop_count.append(str(f"{string}: {count}"))
            

