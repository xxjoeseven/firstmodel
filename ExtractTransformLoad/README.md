### Extract Transform Load

This folder contains the files and results of the ETL process.

As the dataset for the first model was downloaded instead of collected, I went on to write a python script to call the data using etherscan API.

When that was completed, I was curious if I can expand on that to transform the data according to the model's requirement. This is how the folder can about.

* Main.py - this is the main file to executing the code.
* get_data.py - this is the file containing the function to request data using etherscan API.
* api_key.py - this file is not included in this repository because it is my key.
* transform_input.py - this file takes in the collected dataset and transformed it to the model's requirement.
* logConfig.yaml - this yaml file contains my logging configuration both for documentation and for debugging during development
* setupLogger.py - this file sets up the logger
* df2020.csv - this file contains the addresses on MyEtherWallet darklist JSON file that is flagged as fraud in 2020.
* darklist_address.csv - this csv file contains the addresses that has been identified as fraudulent on MyEtherWallet darklist JSON file across the years. (See Main README)
* logfile.log - this is the log file after I ran the codes.
* tx_data_2020.csv - this is the raw dataset that is exported from get_data.py with no transformation.
* transformed_2020_data.csv - this is the transformed dataset ready for prediction using the model.
* add_not_in_list.csv - this file contains addresses identified during the data collection that is not in the darklist, hence they cannot be flagged as fraud.
