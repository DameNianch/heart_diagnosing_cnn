lost_dir=()
lost_num=0

cd ../../data_bank/ecg_ptb/ptbdb       #this directory contains wfdb-ECG file
for num in {001..294}; do       #"294" means the patients number for PTB diagnostic ECG dataset

    if [ -e "patient${num}" ]; then

        cd ./patient"${num}"
        for file in `ls *.dat`; do
            file_name=$(basename ${file} .dat)
            rdsamp -r ${file_name} -c -H -f 0 -v -p >../../csv_format/${file_name}.csv
        done
        cd ..
    
    else
        lost_dir=("${lost_dir[@]}" "patient${num}")
        lost_num=$(( lost_num + 1 ))

    fi

done

if [ ${lost_num} -eq 4 ]; then
    echo "Succeed in convert ALL directories.\(^_^)/"
elif [ ${lost_num} -eq 5 ]; then
    echo "Faild to Download or Convert ONE directory.<(-_-;)>"
else
    echo "Below ${lost_num} directories are not found.(; _ ;)"
    echo "${lost_dir[@]}"
fi
