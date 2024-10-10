# Final Machine Learning
# Import Libraries
import scipy
import numpy as np
import matplotlib
import pandas as pd
import sklearn
import math
import tensorflow as tf
import random
import joblib
import seaborn as sns

# Load libraries
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

# %% Get practice Kaggle Data set
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

# Split data
x_train = x_data[:int(math.floor((len(x_data) * 0.7)))]
y_train = y_data[:int(math.floor((len(y_data) * 0.7)))]
x_valid = x_data[int(math.floor((len(x_data) * 0.7))):int(math.floor((len(x_data) * 0.85)))]
y_valid = y_data[int(math.floor((len(y_data) * 0.7))):int(math.floor((len(x_data) * 0.85)))]
x_test = x_data[int(math.floor((len(x_data) * 0.85))):]
y_test = y_data[int(math.floor((len(y_data) * 0.85))):]

#%%
@tf.keras.utils.register_keras_serializable()
class FCNN(Model):
    def __init__(self):
        super(FCNN, self).__init__()
        self.fcnn = tf.keras.Sequential([
            layers.Dense(7, input_shape=(7,), activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(22, activation='softmax')  # Adjusted output size for multiclass classification
        ])

    def call(self, x):
        output = self.fcnn(x)
        return output

def DefModel():
    return FCNN()

# Save the model



modelClass = DefModel()

# Choose Optimizer
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)


modelClass.compile(optimizer=optimizer,
              loss='binary_crossentropy',
              metrics=['accuracy'])

# %% Model Training
history_m = modelClass.fit(x_train, y_train,
                           validation_data=(x_valid, y_valid),
                           batch_size=64,
                           epochs=300, shuffle=True)

#%%
fig,ax = plt.subplots(1,2,figsize=(14,5))

ax[0].plot(history_m.history['loss'])
ax[0].plot(history_m.history['val_loss'])
ax[0].set_title('model loss')
ax[0].set_ylabel('loss')
ax[0].set_xlabel('epoch')
ax[0].set_yscale('log')
ax[0].legend(['train', 'val'], loc='upper left')

ax[1].plot(history_m.history['accuracy'])
ax[1].plot(history_m.history['val_accuracy'])
ax[1].set_title('model accuracy')
ax[1].set_ylabel('accuracy')
ax[1].set_xlabel('epoch')
ax[1].legend(['train', 'val'], loc='upper left')

#%%
# Generate confusion matrix plot
y_pred = modelClass.predict(x_test)

# Convert predictions to labels
y_pred_labels = np.argmax(y_pred, axis=1)

# Convert one-hot encoded y_test back to labels
y_test_labels = np.argmax(y_test, axis=1)

# Evaluate using confusion matrix
conf_matrix = confusion_matrix(y_test_labels, y_pred_labels)


plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt="d", xticklabels=encoder.classes_, yticklabels=encoder.classes_,annot_kws={"fontsize": 12})
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

# %%
TN = conf_matrix[0, 0]
FP = conf_matrix[0, 1]
FN = conf_matrix[1, 0]
TP = conf_matrix[1, 1]
print([[TN, FP],
 [FN, TP]]
)