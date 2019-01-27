package main

import (
	"encoding/csv"
	"os"
	"io"
	"fmt"
	"log"
	"bufio"
)

//main function
func main(){

	//fmt.Println(os.Args[1])

	//set hyper parameters 
	const disturb_line_num = 2		//This param means explanations for value. For example,input chanels "v1" and voltage unit "mV"
	const disturb_value_num = 0		//For this PTB file,this param means "Elapsed time".
	const use_value_num = 1			//If you use only one value, use this parameter when append-previous-columns.
	const time_window = 5400			//this is a input volume for neural networks
	const slide_time = 5400				//traning data have "overlaped-time".this time calcurate with "time_window"-"slide_time"
	const sampling_freq = 20		//input-data is sampled each this freqency.

	//set some variable
	var cr *csv.Reader
	var cw *csv.Writer
	var columns []string
	var previous_columns []string
	var decimation_columns []string
	var err3 error

	//reading and setting input-file
	input_csv, err1 := os.Open(`../../data_bank/ecg_ptb/csv_format/`+os.Args[1]+`.csv`)	//alter "for-loop-method" after acomplishment of making split-method
	defer input_csv.Close()
	if err1 != nil {
		log.Fatal(err1)
		fmt.Println("this ERROR is on err1")
	}
	cr = csv.NewReader(bufio.NewReader(input_csv))

	//setting output directory and output-file
	output_label, err2 := os.OpenFile(`../../data_bank/ecg_ptb/split_sampling/label_data.csv`, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0666)
	defer output_label.Close()
	if err2 != nil {
		log.Fatal(err2)
		fmt.Println("this ERROR is on err2_label")
	}
	lw := csv.NewWriter(bufio.NewWriter(output_label))

//////////////////////////////////////////////////////////////following code is to read and write CSV files. ////////////////////////////////////////////////

/////////////////////////////////////////////////
//loop for first time to avoid with disturb lines.
/////////////////////////////////////////////////
	
	//setting output directory and output-file
	output_csv, err2 := os.OpenFile(`../../data_bank/ecg_ptb/split_sampling/sampling_data.csv`, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0666)
	defer output_csv.Close()
	if err2 != nil {
		log.Fatal(err2)
		fmt.Println("this ERROR is on err2")
	}
	cw = csv.NewWriter(bufio.NewWriter(output_csv))
	for j:=0 ;j<disturb_line_num;j++{
		columns, err3 = cr.Read()
	}

	//Previous line value are not exist.
	//All current-window values are saved.
	for j := 0; j<time_window ; j++{
		columns, err3 = cr.Read()
		atai := columns[use_value_num]
		previous_columns = append(previous_columns, atai)
		if err3 == io.EOF{
			log.Fatal(err3)
			fmt.Println("this ERROR happen on err3.")
		}
	}
	
	//Write all data each sampling time.
	for j := 0; j*sampling_freq<time_window ; j++{
		decimation_columns = append(decimation_columns, previous_columns[ j*sampling_freq ])
	}	
	cw.Write(decimation_columns)
	lw.Write(os.Args[2:])
	//fmt.Println(os.Args)


////////////////////////////////////////////////////////////////////
//using previous values and saving current values for next step i++.
///////////////////////////////////////////////////////////////////
	for k:=1;;k++{
		//do flush before running k loop
		var decimation_columns []string
		cw.Flush()
		lw.Flush()

		//Delete some previous values(columns) which is not used.
		previous_columns = append(previous_columns[slide_time:])

		//setting output directory and output-file
		if err2 != nil {
			log.Fatal(err2)
			fmt.Println("this ERROR is on err2")
		}
		cw = csv.NewWriter(bufio.NewWriter(output_csv))

		//read the input-file and save the values, and stop this loop to read the file if it is EOF 
		for i:=0 ;i<slide_time; i++ {
			columns,err3 = cr.Read()
			if err3 == io.EOF{
				break
			}
			atai := columns[use_value_num]
			previous_columns = append(previous_columns, atai)
		}

		//Writing all value in the time_window.
		for j := 0; j*sampling_freq<time_window ; j++{
			if err3 == io.EOF{
				break
			}
			decimation_columns = append(decimation_columns, previous_columns[ j*sampling_freq ])
		}
		if err3 != io.EOF{
			cw.Write(decimation_columns)
			lw.Write(os.Args[2:])
		}

		//Processing for EOF. Here, a imcomplete file is remove.
		if err3 == io.EOF{
			break
		}
		
		//buffer ERROR is exported here.
		if err := cw.Error(); err != nil {
			log.Fatalln("error writing csv:", err)
		}
	}


}