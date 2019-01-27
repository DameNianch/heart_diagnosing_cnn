import tensorflow as tf
import numpy as np
import os
import datetime
import model_and_opt as MandOp
import takin_data as Takind
import result_summary as Resm


def main():

    # decide constant params
    FILTER_SIZE = 30        
    EPOCH_TIMES = 1        
    TRAIN_BATCH_NUM = 1      
    LEARNING_RATE = 0.1
    DROPOUT_RATE_TRAIN = 0.7
    VALID_DATA_RATE = 1
    DROPOUT_RATE_VALID = 1.0
    NUM_CLASS = 10

    # label_number is same to NUM_CLASS
    x, y, valid_x, valid_y,time_window, label_number, class_weights, valid_data_num = Takind.mkdata(FILTER_SIZE, EPOCH_TIMES, TRAIN_BATCH_NUM)

    #setting placeholder
    input_placeholder = tf.placeholder(tf.float32, shape=(time_window, None))
    true_label_placeholder = tf.placeholder(tf.float32, shape=(None, label_number))
    drop_rate_placeholder = tf.placeholder(tf.float32)

    #setting models
    inference_value = MandOp.graph_tf(input_placeholder, drop_rate_placeholder, NUM_CLASS)
    loss_calc = MandOp.loss_calc(true_label_placeholder, inference_value)
    train_opt = MandOp.train_opt(loss_calc, LEARNING_RATE)
    valid_calc = MandOp.valid_acc_calc(true_label_placeholder, inference_value, NUM_CLASS)

    #define tensorflow something and initilizing variables
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    #from this line, starting training 
    for i_step in range(EPOCH_TIMES):
        x_train = x[0]
        y_train = y[0]
        sess.run(train_opt, feed_dict={input_placeholder: x_train, true_label_placeholder: y_train, drop_rate_placeholder: DROPOUT_RATE_TRAIN})
        
        # for j_valid in range(int(VALID_DATA_RATE*valid_data_num)):
        for j_valid in range(1):
            x_valid = valid_x[j_valid]
            y_valid = valid_y[j_valid]
            validation_results, tmp_ignore = sess.run(valid_calc, feed_dict={input_placeholder: x_valid, true_label_placeholder: y_valid, drop_rate_placeholder: DROPOUT_RATE_VALID})
        print("step=%d \t acc=%.2f" % (i_step, validation_results))
    
    
    #after training and validation, sammarizing results with validation data
    predict_y = []
    test_y = []

    for j_valid in range(int(valid_data_num*VALID_DATA_RATE)):

        x_valid = valid_x[j_valid]
        y_valid = valid_y[j_valid]
        validation_results = sess.run(inference_value, feed_dict={input_placeholder: x_valid,  drop_rate_placeholder: DROPOUT_RATE_VALID})
        predict_y.extend(validation_results.tolist())
        test_y.extend(y_valid.tolist())
    
    predict_and_true = Resm.Predict_and_True(predict_y, test_y)
    predict_and_true.confusion_mx_writer()


    sess.close()


if __name__== "__main__":
    main()