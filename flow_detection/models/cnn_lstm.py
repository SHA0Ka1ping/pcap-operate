import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import scikitplot as skplt
import matplotlib.pyplot as plt
import pickle as pk
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Embedding, LSTM, GlobalAveragePooling2D
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPool1D, BatchNormalization, Bidirectional
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import read_data
from sklearn.preprocessing import MinMaxScaler
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

use_data,data_labels,base_info=read_data.gen_data_label()
data_labels=read_data.num_labels(data_labels)
use_data=use_data.values
use_data.astype('float32')
data_labels=data_labels.values

scaler=MinMaxScaler()
scaler.fit_transform(use_data)
X_train, X_test, y_train, y_test = train_test_split(use_data, data_labels, test_size=0.25,
                                                    shuffle=True, random_state=42)
model= Sequential()
# model.add(Embedding(input_dim=1000000,output_dim=128,input_length=X_train.shape[1], name='layer_embedding'))
model.add(BatchNormalization())
flstm = LSTM(128, return_sequences=True)  # go_backwards 默认为false
# blstm = LSTM(256, go_backwards=True, return_sequences=True)
# 注意前后lstm的 go_backwards 必须设置不同，一个为false一个为true
# bilstm_layer = Bidirectional(LSTM(units=256, return_sequences=True),merge_mode='concat')
# model.add(bilstm_layer)
model.add(layer=Bidirectional(LSTM(256, return_sequences=True),merge_mode='concat'))
model.add(flstm)
model.add(Dense(64, activation=tf.nn.relu))
model.add(Dense(units=1, activation='sigmoid'))
optimizer = Adam(lr=.0001)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.build((None, 20, 78))
model.summary()

