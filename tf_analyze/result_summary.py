import numpy as np
from sklearn.metrics import confusion_matrix

class Predict_and_True:
    def __init__(self, predict_y, valid_y):
        
        self.predict_y = predict_y
        self.valid_y = valid_y

    def confusion_mx_writer(self):
        
        y_true = self.valid_y
        y_pred = self.predict_y
        y_true = np.argmax(y_true, axis=1)
        y_pred = np.argmax(y_pred, axis=1)

        label=sorted(list(set(y_true)))
        print("[*] Confusion matrix")
        conf_mat_data=confusion_matrix(y_true, y_pred,labels=label)
        print(conf_mat_data)