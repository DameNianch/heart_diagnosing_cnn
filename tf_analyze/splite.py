import numpy as np
import os
import math
import csv
from sklearn.model_selection import train_test_split

#パラメータ設定
Test_Rate = 0.2

#読み込みファイル設定
FILE_IN = open('/your_dir', 'r')
FILE_OUT = open('/your_dir', 'r')
whats_input = csv.reader(FILE_IN, quoting = csv.QUOTE_NONNUMERIC)
whats_output = csv.reader(FILE_OUT, quoting = csv.QUOTE_NONNUMERIC)
#書き込みファイル設定
data_for_train = open('/your_dir','w')
label_for_train = open('/your_dir','w')
data_for_valid = open('/your_dir','w')
label_for_valid = open('/your_dir','w')


#データ
input_data = []
output_data = []
#time_window, label_numberを自動取得するために、最初のデータだけ別処理
value_sub = next(whats_input)      #入力値ファイル読み込み
label_sub = next(whats_output)     #出力値ファイル読み込み  
time_window = len(value_sub)
label_number = len(label_sub)
#入出力データのappend
input_data.append(value_sub)
output_data.append(label_sub)

#２番目のデータから最後まで取得するループ
data_number = 1
while True:
    try:
    #for ii in range (DATA_MAX):
        value_sub = next(whats_input)      #入力値ファイル読み込み
        label_sub = next(whats_output)     #出力値ファイル読み込み
        input_data.append(value_sub)
        output_data.append(label_sub)
        #print(label_sub)
        data_number += 1
    except StopIteration:
        break
#データ数、時間窓、パラメータ数（ラベル数）の表示
print("\n All_DATA_Num = "+str(data_number)+"\t TIME_WINDOW = "+str(time_window)+"\t LABEL_Num = "+str(label_number)+"\n\n")

#sklearnでデータの分割
train_data, valid_data, train_label, valid_label =train_test_split( input_data, output_data, test_size = Test_Rate )

#学習データ分割出力
DT = csv.writer(data_for_train, lineterminator='\n')
DT.writerows(train_data)
PT = csv.writer(label_for_train, lineterminator='\n')
PT.writerows(train_label)
train_data_number = len(train_data)
train_label_number = len(train_label)
print("finish train_data")
print("  TEST_DATA_Num = "+str(train_data_number)+"\t TEST_LABEL_Num = "+str(train_label_number)+"\n\n")

#検証データ分割出力
DV = csv.writer(data_for_valid, lineterminator='\n')
DV.writerows(valid_data)
PV = csv.writer(label_for_valid, lineterminator='\n')
PV.writerows(valid_label)
valid_data_number = len(valid_data)
valid_label_number = len(valid_label)
print("finish valid_data")
print("  VALID_DATA_Num = "+str(valid_data_number)+"\t VALID_LABEL_Num = "+str(valid_label_number)+"\n\n")

print("\n Finish Spliting Data \n\n\n\n")
FILE_IN.close()
FILE_OUT.close()
data_for_train.close()
data_for_valid.close()
label_for_train.close()
label_for_valid.close()