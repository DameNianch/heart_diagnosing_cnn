import csv
from sklearn import preprocessing
import numpy as np
from sklearn.utils import class_weight


data_for_train = open('/your_dir','r')
label_for_train = open('/your_dirv','r')
data_for_valid = open('/your_dir','r')
label_for_valid = open('/your_dirv','r')
print("finish opening all files")
DT = csv.reader(data_for_train, quoting = csv.QUOTE_NONNUMERIC)
print("DT is read")
PT = csv.reader(label_for_train, quoting = csv.QUOTE_NONNUMERIC)
DV = csv.reader(data_for_valid, quoting = csv.QUOTE_NONNUMERIC)
PV = csv.reader(label_for_valid, quoting = csv.QUOTE_NONNUMERIC)
print("All data are read")
MMScaler = preprocessing.MinMaxScaler()     
#MMScaler = preprocessing.StandardScaler()  #くそつかえない。


def mkdata(filter_size, epoch_times, train_batch_num):

    ################################学習データ読み込み
    train_data = []
    train_label = []

    #time_window, label_numberを自動取得するために、最初のデータだけ別処理
    value_sub = next(DT)
    label_sub = next(PT) 
    time_window = len(value_sub)
    label_number = len(label_sub)
    #入出力データのappend
    train_data.append(value_sub)
    train_label.append(label_sub)
    
    #２番目のデータから最後まで取得するループ
    data_number = 1
    all_count = 1
    while True:
        try:
        #for ii in range (DATA_MAX):
            value_sub = next(DT)      #入力値ファイル読み込み
            label_sub = next(PT)     #出力値ファイル読み込み
            train_data.append(value_sub)
            train_label.append(label_sub)
            #print(label_sub)
            data_number += 1
            all_count += 1
            #print(all_count)
        except StopIteration:
            break
    train_num = data_number
    print("finish reading training_data")


    ################################検証データ読み込み
    valid_data = []
    valid_label = []

    data_number = 0
    while True:
        try:
            value_sub = next(DV)      #入力値ファイル読み込み
            label_sub = next(PV)     #出力値ファイル読み込み
            valid_data.append(value_sub)
            valid_label.append(label_sub)
            data_number += 1
            all_count += 1
            #print(all_count)
        except StopIteration:
            break
    valid_data_num = data_number
    print("finish reading validation_data")

    ####################データ数、時間窓、パラメータ数（ラベル数）の表示
    print("\n ALL_DATA_Num = "+str(all_count)+"\t Train_DATA_Num = "+str(train_num)+"\t Valid_DATA_Num = "+str(valid_data_num)+"\n")
    print("\t TIME_WINDOW = "+str(time_window)+"\t labelETER_Num = "+str(label_number)+"\n\n")



    """
    #sklearnで絶対値の最大値が１となるように正規化
    scaled_DT = MMScaler.fit_transform(train_data)
    scaled_PT = MMScaler.fit_transform(train_label)
    scaled_DV = MMScaler.fit_transform(valid_data)
    scaled_PV = MMScaler.fit_transform(valid_label)
    print("finish scaling all data")
    """
    scaled_DT = train_data
    scaled_PT = train_label
    scaled_DV = valid_data
    scaled_PV = valid_label
    
    x_f = np.asarray(scaled_DT)
    x = x_f.reshape(-1, time_window, 1)
    xv_f = np.asarray(scaled_DV)
    xv = xv_f.reshape(-1, time_window, 1)
    y_f = np.array(scaled_PT)
    y = y_f.reshape(-1, 1, label_number)
    yv_f = np.array(scaled_PV)
    yv = yv_f.reshape(-1, 1, label_number)
    print("Change numpy array")
    

    argment_label = [yi.argmax() for yi in y]
    class_weights_list = class_weight.compute_class_weight(
        'balanced',
        np.unique(argment_label),
        argment_label
        )
    #print(np.power(class_weights_list,2))
    class_weights = dict(zip(np.unique(argment_label), np.power(class_weights_list,1.0)))
    print(class_weights)
    #print(np.unique(argment_label))

    data_for_train.close()
    data_for_valid.close()
    label_for_train.close()
    label_for_valid.close()

    print("End of closing all file")

    return x, y, xv, yv, time_window, label_number, class_weights, valid_data_num