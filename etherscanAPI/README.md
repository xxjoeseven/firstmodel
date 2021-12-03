### Data collection through Etherscan API

The objective of this exercise is to collect transaction data of ethereum address on the darklist by MyEtherWallet.

https://github.com/MyEtherWallet/ethereum-lists/blob/master/src/addresses/addresses-darklist.json

The data is collected to through etherscan API.

https://etherscan.io/apis

### Data Collection Process

1) darklist addresses are extracted from MyEtherWallet github into a jupyter notebook.
2) duplicate addresses are dropped and the remaining addresses are saved to a csv file.
3) created an account with etherscan to create the API key.
4) three python scripts are written to collect the necessary data.

### Scripts

1) run.py is the main file to call the collection function.
2) get_data.py is the function which takes in a Series of ethereum addresses and loop through to collect the data.
3) api_key is the file that contains and return my api key which is not included in this repository.

### Note on Development

In order to refrain from always calling the etherscan API unnecessarily, a text file with etherscan JSON response is created to simulate etherscan response. 
