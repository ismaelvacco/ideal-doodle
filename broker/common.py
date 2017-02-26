import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s %(message)s',filename='var/log/arbitragem.log', filemode='w', level=logging.INFO)


def getLogging():
    return logging
