import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import scikitplot as skplt
import matplotlib.pyplot as plt
import pickle as pk
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Embedding, LSTM, GlobalAveragePooling2D
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPool1D, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import read_data

use_data,data_labels=read_data.gen_data_label()
data_labels=read_data.num_labels(data_labels)
X_train, X_test, y_train, y_test = train_test_split(use_data, data_labels, test_size=0.25,
                                                    shuffle=True, random_state=42)
print(X_train.shape,y_train.shape)
