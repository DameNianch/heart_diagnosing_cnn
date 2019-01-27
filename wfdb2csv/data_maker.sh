cd ../../data_bank/ecg_ptb/split_sampling
rm -rf ./*.csv
cd ../csv_format       #this directory contains wfdb-ECG file

for file in `ls *.csv`; do
    name=$(basename ${file} .csv)
    cd ../header_useful
    #tr -d ' ' < ${name}.hea > ${name}2.hea
    line=`grep Reason ${name}_useful.hea`
    cd ../../../git_data/ECG-wfdb2csv
    label=${line:20}
    # echo $label
    
##########Label classfication##############
    #Myocardial infarction
    #Cardiomyopathy
    #Heart failure	
    #Bundle branch block
    #Dysrhythmia
    #Myocardial hypertrophy
    #Valvular heart disease
    #Myocarditis
    #Miscellaneous
    #Healthy controls
    #n/a
    if [ $(echo "${label}" | grep -e "Myocardialinfarction") ]; then
        go run splitter.go ${name} 1 0 0 0 0 0 0 0 0 0
    elif [ $(echo "${label}" | grep -e "Cardiomyopathy") ]; then
        go run splitter.go ${name} 0 1 0 0 0 0 0 0 0 0
    elif [ $(echo "${label}" | grep -e "Heartfailure") ]; then
        go run splitter.go ${name} 0 0 1 0 0 0 0 0 0 0 
    elif [ $(echo "${label}" | grep -e "Bundlebranchblock") ]; then
        go run splitter.go ${name} 0 0 0 1 0 0 0 0 0 0
    elif [ $(echo "${label}" | grep -e "Dysrhythmia") ]; then
        go run splitter.go ${name} 0 0 0 0 1 0 0 0 0 0
    elif [ $(echo "${label}" | grep -e "ypertrophy") ]; then
        go run splitter.go ${name} 0 0 0 0 0 1 0 0 0 0
    elif [ $(echo "${label}" | grep -e "Valvularheartdisease") ]; then
        go run splitter.go ${name} 0 0 0 0 0 0 1 0 0 0
    elif [ $(echo "${label}" | grep -e "Myocarditis") ]; then
        go run splitter.go ${name} 0 0 0 0 0 0 0 1 0 0
    elif [ $(echo "${label}" | grep -e "Stableangina") ]; then
        go run splitter.go ${name} 0 0 0 0 0 0 0 0 1 0
    elif [ $(echo "${label}" | grep -e "Healthycontrol") ]; then
        go run splitter.go ${name} 0 0 0 0 0 0 0 0 0 1
    elif [ $(echo "${label}" | grep -e "n/a") ]; then
        :
    else
        echo $label
        echo $name
    fi

    cd ../../data_bank/ecg_ptb/csv_format       #this directory contains wfdb-ECG file
done