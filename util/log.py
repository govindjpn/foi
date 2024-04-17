import logging
from datetime import datetime as dt



log_file_name = 'FOI.log'
logging.basicConfig(filename=log_file_name, filemode='w', level=logging.DEBUG)
logging.info("Program Start")

def log_write (s):
    logging.debug(f'{dt.now().strftime("%d/%m/%Y %H:%M:%S %f")} {s}')