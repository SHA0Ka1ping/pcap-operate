import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
import read_data
from sklearn.metrics import make_scorer, fbeta_score
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import pickle as pk
from sklearn.preprocessing import MinMaxScaler

use_data,data_labels,base_info=read_data.gen_data_label()
data_labels=read_data.num_labels(data_labels)
use_data=use_data.values
use_data=use_data.astype(float)
data_labels=data_labels.values
data_labels=data_labels.astype(float)


classes=[0.0,1.0,3.0,4.0,5.0]
weight = compute_class_weight(class_weight = 'balanced', classes=classes, y=data_labels)
print(weight)

scaler=StandardScaler()
use_data=scaler.fit_transform(use_data)
use_data=use_data.astype(float)
print(use_data)
X_train, X_test, y_train, y_test = train_test_split(use_data, data_labels, test_size=0.25,
                                                    shuffle=True, random_state=42)
X_train=X_train.astype(str)
X_test=X_test.astype(str)
y_train=y_train.astype(str)
y_test=y_test.astype(str)
f1_score = make_scorer(fbeta_score, beta=1)
model=svm.SVC(C=2, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True,
                probability=False, tol=0.001, cache_size=200, class_weight={"0.0":2.72133978e-01,"1.0":7.07392901e+00,"3.0":1.45589050e+00,"4.0":2.01513250e+00,
 "5.0":1.15588000e+03},
                verbose=False, max_iter=-1, decision_function_shape="ovr",
                random_state=None)
model.fit(X_train,y_train)
with open("svm.pickle", 'wb') as file:
    pk.dump(model, file)
y_pred = model.predict(X_test)

print("model classification report: \n\n {}".format(classification_report(np.array(y_test), y_pred.flatten())))
