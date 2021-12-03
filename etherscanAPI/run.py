import pandas as pd
from get_data import get_tx_data

ether_addresses = pd.read_csv('darklist_address.csv')  # data downloaded from MyEtherWallet github
ether_addresses = ether_addresses.squeeze()  # convert to Series

df = get_tx_data(ether_addresses)

df.to_csv('darklist_data.csv', index=False)

print('Task Complete')
