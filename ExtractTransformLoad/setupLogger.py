def set_up_logging():

    import logging.config
    import yaml
    with open('logConfig.yaml', 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
