import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
import read_data
from sklearn.metrics import make_scorer, fbeta_score
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import pickle as pk
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
class retrainModel(object):
    def __init__(self,data_dir):
        self.data_dir=data_dir
    def load_data(self):
        database=read_data.getData(self.data_dir)
        database.gen_total_data()
        return database.gen_data_label(self.path)
    def class_weight(self,labels):
        cnt=Counter(labels)
        classes=[]
        for k in cnt.keys():
            classes.append(k)
        weight = compute_class_weight(class_weight='balanced', classes=classes, y=labels)
        weight_dict={}
        for i in range(len(classes)):
            dict[classes[i]]=weight[i]
        return weight_dict
    def trainModel(self):
        use_data, data_labels, base_info = self.load_data()
        # data_labels = read_data.num_labels(data_labels)
        use_data = use_data.values
        use_data = use_data.astype(float)
        data_labels = data_labels.values
        data_labels = data_labels.astype(float)
        classWeight=self.class_weight(data_labels)
        scaler = StandardScaler()
        use_data = scaler.fit_transform(use_data)
        use_data = use_data.astype(float)
        X_train, X_test, y_train, y_test = train_test_split(use_data, data_labels, test_size=0.25,
                                                            shuffle=True, random_state=42)
        X_train = X_train.astype(str)
        X_test = X_test.astype(str)
        y_train = y_train.astype(str)
        y_test = y_test.astype(str)
        f1_score = make_scorer(fbeta_score, beta=1)
        model = svm.SVC(C=2, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True,
                        probability=False, tol=0.001, cache_size=200,
                        class_weight=classWeight,
                        verbose=False, max_iter=-1, decision_function_shape="ovr",
                        random_state=None)
        model.fit(X_train, y_train)
        with open("svm.pickle", 'wb') as file:
            pk.dump(model, file)
        y_pred = model.predict(X_test)
        print("model classification report: \n\n {}".format(classification_report(np.array(y_test), y_pred.flatten())))

