def get_tx_data(ether_addresses):
    """ 
    Get transaction data using ethereum account address through etherscan API.

    :param ether_addresses:

        list or Series of ether addresses

    :return:

        A dataframe of collected transaction data ['timestamp', 'from_add', 'to_add', 'value']

    """

    from api_key import etherscan_key  # Not included in repo, it is a simple return function of API key
    import pandas as pd
    import requests
    # import json (required during development to read JSON file to refrain from always calling etherscan API)
    import time
    import logging

    logger = logging.getLogger(__name__)
    logger.info('Logging is configured.')

    dataset = pd.DataFrame(columns=['timestamp',
                                    'from_add',
                                    'to_add',
                                    'value'])

    for ether_address in ether_addresses:

        page_no = 1
        # Get data from etherscan.io with a while loop that increases the page number by 1 until response message
        # is not 'OK'
        while page_no > 0:

            url = 'https://api.etherscan.io/api?module=account&action=txlist&address=' + ether_address + \
                  '&startblock=0&endblock=99999999&page=' + str(page_no) + \
                  '&offset=10&sort=asc&apikey=' + etherscan_key()
            data = requests.get(url)

            if data.status_code != 200:
                logger.info('Status Code is not 200, it is ' + str(data.status_code))
                break

            data = data.json()
            time.sleep(1)  # give 1 second before starting the next line.

            if data['message'] != 'OK':
                logger.info('message is not OK')  # if data['message'] != 'OK', it means there is no more transactions.
                break

            # for development purposes, to refrain from always calling the etherscan api
            # with open('tx_data.txt') as json_file:
            #     data = json.load(json_file)
            # pretty_data = json.dumps(data, indent=4)

            for x in data['result']:
                timestamp = x['timeStamp']
                from_add = x['from']
                to_add = x['to']
                value = x['value']

                dataset = dataset.append({'timestamp': timestamp,
                                          'from_add': from_add,
                                          'to_add': to_add,
                                          'value': value},
                                         ignore_index=True)

            logger.info(ether_address + ' Page ' + str(page_no) + ' Completed.')
            page_no += 1

        logger.info('Extraction for ' + ether_address + ' done.')

    return dataset
