cd ../../data_bank/ecg_ptb/ptbdb

for num in {001..294}; do       #"294" means the patients number for PTB diagnostic ECG dataset

    if [ -e "patient${num}" ]; then

        cd ./patient"${num}"
        for file in `ls *.hea`; do
            cp $file ../../headers/$file
        done
        cd ../
    
    else
        lost_dir=("${lost_dir[@]}" "patient${num}")
        lost_num=$(( lost_num + 1 ))

    fi

done

if [ ${lost_num} -eq 4 ]; then
    echo "Succeed in copy ALL header file.\(^_^)/"
elif [ ${lost_num} -eq 5 ]; then
    echo "Faild to copy ONE directory.<(-_-;)>"
else
    echo "Below ${lost_num} directories are not found.(; _ ;)"
    echo "${lost_dir[@]}"
fi