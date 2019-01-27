cd ../../data_bank/ecg_ptb/header_useful
rm -rf ./*.hea
cd ../headers       #this directory contains wfdb-ECG file

for file in `ls *.hea`; do
    name=$(basename ${file} .hea)
    tr -d ' ' < ${name}.hea > ../header_useful/${name}_useful_sub.hea
    sed -e "24,69d" ../header_useful/${name}_useful_sub.hea > ../header_useful/${name}_useful_sub2.hea
    sed -e "1,22d" ../header_useful/${name}_useful_sub2.hea > ../header_useful/${name}_useful.hea
    rm ../header_useful/${name}_useful_sub.hea
    rm ../header_useful/${name}_useful_sub2.hea
done