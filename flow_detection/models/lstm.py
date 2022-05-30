import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import scikitplot as skplt
import matplotlib.pyplot as plt
import pickle as pk
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.layers import Embedding, LSTM, GlobalAveragePooling2D
from tensorflow.keras.layers import Dense, Dropout, Conv1D, MaxPool1D, BatchNormalization, Bidirectional
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import read_data
from sklearn.preprocessing import MinMaxScaler
import os
from keras.utils import to_categorical

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
config.gpu_options.per_process_gpu_memory_fraction = 0.3
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

use_data,data_labels,base_info=read_data.gen_data_label()
data_labels=read_data.num_labels(data_labels)
use_data=use_data.values
use_data=use_data.astype(float)
# data_labels=data_labels.astype(float)
data_labels=data_labels.values
flstm = LSTM(128, return_sequences=True, activation=tf.nn.relu)  # go_backwards 默认为false
scaler=MinMaxScaler()
use_data=scaler.fit_transform(use_data)
X_train, X_test, y_train, y_test = train_test_split(use_data, data_labels, test_size=0.25,
                                                    shuffle=True, random_state=42)
X_train=np.reshape(X_train,(X_train.shape[0],79))
X_test=np.reshape(X_test,(X_test.shape[0],79))
model= Sequential()
model.add(Embedding(input_dim=100000,output_dim=64,input_length=X_train.shape[1], name='layer_embedding'))
model.add(BatchNormalization())
model.add(Conv1D(filters = 32, kernel_size = 9, padding = 'same', activation = 'relu'))
model.add(MaxPool1D(pool_size = 2))
model.add(Dropout(0.1))
# model.add(flstm)
model.add(Dropout(0.1))
# model.add(Conv1D(filters = 32, kernel_size = 9, padding = 'same', activation = 'relu'))
# model.add(MaxPool1D(pool_size = 2))
# model.add(layer=Bidirectional(LSTM(128,return_sequences=False,activation=tf.nn.relu),merge_mode='concat'))
model.add(Dropout(0.1))

model.add(Dense(units=6, activation='softmax'))

optimizer = Adam(lr=0.05)

sgd = SGD(lr=0.05,decay=1e-6,momentum=0.9,nesterov=True)
y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)
#y_train=tf.one_hot(y_train, depth=6),


model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.build((None,20,79))
model.summary()
history = model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=64)
model.save('flow_detection_model.h5')


fig, ax = plt.subplots(1,2, figsize=[12,6])
ax[0].plot(history.history["loss"])
ax[0].plot(history.history["val_loss"])
ax[0].set_title(" Loss")
ax[0].legend(("Training", "validation"), loc="upper right")
ax[0].set_xlabel("Epochs")
ax[1].plot(history.history["accuracy"])
ax[1].plot(history.history["val_accuracy"])
ax[1].legend(("Training", "validation"), loc="lower right")
ax[1].set_title("Accuracy")
ax[1].set_xlabel("Epochs")
plt.show()
y_pred = model.predict_classes(X_test)
print("model classification report: \n\n {}".format(classification_report(np.array(y_test), y_pred.flatten())))