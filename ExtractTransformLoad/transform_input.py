def transform_data(dataset, address_check):
    """
    Ingest collected transaction data and transform the data according to the ML model requirement.
    Checks the address with the darklist_address csv and flag 1 if found, flag 0 if not found.


    :param dataset:

    A Pandas DataFrame of extracted Ether transactions record.

    :param address_check:

    List or Series of Ether addresses passed in for data extraction.

    :return:

    A tuple that contains the following:
        A Pandas DataFrame of transformed data that can be fit into the ML Model.
        A list of ether addresses that is not in the original list of Ether addresses passed in.

    """

    # import json # Use only during development to refrain from calling API unnecessarily
    import pandas as pd
    import datetime
    import logging

    logger = logging.getLogger(__name__)
    logger.info('Logging is configured')

    dark_add = pd.read_csv('darklist_address.csv')
    # convert address to lowercase to match return data format from Etherscan
    dark_add = dark_add['address'].str.lower()

    # Create empty dataframe with column names according to ML model requirements to append transformed data
    transformed_data = pd.DataFrame(columns=['flag', 'sent_tnx', 'total_transactions_(including_tnx_to_create_contract',
                                             'min_val_sent', 'received_tnx', 'avg_val_sent',
                                             'avg_min_between_received_tnx',
                                             'avg_val_received', 'min_val_received', 'unique_received_from_addresses',
                                             'time_diff_between_first_and_last_(min)'])

    # with open('tx_data.txt') as json_file: # Use only during development to refrain from calling API unnecessarily
    #     data = json.load(json_file)
    #     # pretty_data = json.dumps(data, indent=4)

    # Drop duplicate due to double collection because of from_add and to_add
    dataset.drop_duplicates(inplace=True)

    # convert timestamp to datetime object
    dataset.loc[:, 'timestamp'] = pd.to_datetime(dataset['timestamp'], unit='s')

    # convert value to float. some values may be too large to convert to int.
    dataset['value'] = dataset['value'].astype(float)

    # convert value from wei to ether
    dataset.loc[:, 'value'] = dataset['value'].div(1000000000000000000)

    logger.info('Data type conversion completed.')

    print(dataset.head())

    # Extract the list of all ether_addresses from dataset 'from_add' & 'to_add' columns to loop for transformation
    # Only unique address is recorded. The address from Etherscan are all in lowercase.
    to_add_list = dataset.loc[:, 'to_add']
    from_add_list = dataset.loc[:, 'from_add']
    all_add_list = pd.concat([to_add_list, from_add_list])
    all_add_list = all_add_list.unique()

    # all_add_list is an extraction of all addresses.
    logger.info('All unique addresses extracted from Etherscan returned data')

    # convert address to lowercase to match return data format from Etherscan
    address_check = address_check.str.lower()
    logger.info('Known Address check database converted to lowercase to match Etherscan returned data')

    not_in_original_list = []

    for ether_address in all_add_list:

        if ether_address not in address_check.values:  # check if address was initially passed in.
            not_in_original_list.append(ether_address)  # record the addresses that is not passed in.
            continue

        if ether_address in dataset['to_add'].values:
            to_add_data = dataset.loc[dataset['to_add'] == ether_address]
        else:
            to_add_data = pd.DataFrame([])

        logger.info('to_add_data reached')

        if ether_address in dataset['from_add'].values:
            from_add_data = dataset.loc[dataset['from_add'] == ether_address]
        else:
            from_add_data = pd.DataFrame([])

        logger.info('from_add_data reached')

        # Create temp dataset for each ether_address for transformation - easy to calculate time differences
        temp_dataset = pd.concat([to_add_data, from_add_data])

        logger.info('Concat ' + ether_address + ' from_add & to_add into temp_dataset')

        # Total number of transactions
        total_tx = len(temp_dataset)

        # Time difference between first and last transaction
        if total_tx > 1:
            time_diff = temp_dataset.iloc[-1, 0] - temp_dataset.iloc[0, 0]
            time_diff_between_first_last_tx = time_diff / datetime.timedelta(minutes=1)
        else:
            time_diff_between_first_last_tx = 0.0

        # ether_address = # Only use for development purposes

        # to_add section
        if ether_address in temp_dataset['to_add'].values:
            # Average value in Ether ever received
            avg_val_rec = temp_dataset.loc[temp_dataset['to_add'] == ether_address]['value'].mean()
            # Minimum value in Ether ever received
            min_val_rec = temp_dataset.loc[temp_dataset['to_add'] == ether_address]['value'].min()
            # Total Unique Addresses from which account received transactions
            unique_rec_from_add = len(temp_dataset.loc[temp_dataset['to_add'] == ether_address]['from_add'].unique())
            # Total number of received normal transactions
            received_tx = len(temp_dataset.loc[temp_dataset['to_add'] == ether_address])
            # Average time between received transactions for account in minutes
            if received_tx > 1:  # prevent NaN result due to only 1 received transaction unable to .diff()
                difference = temp_dataset.loc[temp_dataset['to_add'] == ether_address]['timestamp'].diff()
                avg_min_between_rec_tx = difference.mean() / datetime.timedelta(minutes=1)
            else:
                avg_min_between_rec_tx = 0
        else:
            avg_val_rec = 0.0
            min_val_rec = 0.0
            avg_min_between_rec_tx = 0.0
            unique_rec_from_add = 0.0
            received_tx = 0.0

        # from_add section
        if ether_address in temp_dataset['from_add'].values:
            # Average value of Ether ever sent
            avg_val_sent = temp_dataset.loc[temp_dataset['from_add'] == ether_address]['value'].mean()
            # Minimum value of Ether ever sent
            min_val_sent = temp_dataset.loc[temp_dataset['from_add'] == ether_address]['value'].min()
            # Total number of sent normal transactions
            sent_tx = len(temp_dataset.loc[dataset['from_add'] == ether_address])
        else:
            avg_val_sent = 0.0
            min_val_sent = 0.0
            sent_tx = 0.0

        if ether_address in dark_add.values:
            flag = 1
        else:
            flag = 0

        # Append transformed data to DataFrame
        transformed_data = transformed_data.append({'flag': flag,
                                                    'sent_tnx': sent_tx,
                                                    'total_transactions_(including_tnx_to_create_contract': total_tx,
                                                    'min_val_sent': min_val_sent,
                                                    'received_tnx': received_tx,
                                                    'avg_val_sent': avg_val_sent,
                                                    'avg_min_between_received_tnx': avg_min_between_rec_tx,
                                                    'avg_val_received': avg_val_rec,
                                                    'min_val_received': min_val_rec,
                                                    'unique_received_from_addresses': unique_rec_from_add,
                                                    'time_diff_between_first_and_last_(min)':
                                                        time_diff_between_first_last_tx},
                                                   ignore_index=True)

    return transformed_data, not_in_original_list
