import pandas as pd
import csv
import logging
from setupLogger import set_up_logging
from get_data import get_tx_data
from transform_input import transform_data

set_up_logging()

logger = logging.getLogger(__name__)
logger.info('Logger set up')

ether_addresses = pd.read_csv('df2020.csv')  # data downloaded from MyEtherWallet github filtered year 2020
ether_addresses = ether_addresses.squeeze()  # convert to Series

df = get_tx_data(ether_addresses)  # function call etherscan API for the transaction data

# log the return transaction data as a Dataframe
logger.info('TX Dataset collected and returned as a Dataframe, export the TX Data to csv')
df.to_csv('tx_data_2020.csv', index=False)

# if we want to pass in a dataset instead of an API call for debugging transform_input
# df = pd.read_csv('tx_data_2020.csv')

# df is the dataset collected, ether_addresses are the addresses passed in
return_tuple = transform_data(df, ether_addresses)
(df_transform, add_not_in_list) = return_tuple  # unpack the returned tuple from transform_data
logger.info('Return tuple unpacked')


# export the transformed data to csv
df_transform.to_csv('transformed_2020_data.csv', index=False)
logger.info('Transformed Data exported to csv')

# write add_not_in_list to a csv file
with open('add_not_in_list.csv', 'w') as file:
    write = csv.writer(file)
    write.writerows([add_not_in_list])

logger.info('Addresses not in original list written to csv')
logger.info('Task Complete')
