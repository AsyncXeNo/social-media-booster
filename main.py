import config as _

import time

import selenium_utils

from loguru import logger

from accounts.google import create_google_account
from api.smsactivate import get_active_activation_by_phone_number, get_balance


if __name__ == '__main__':

    # driver = selenium_utils.get_chromedriver_without_proxy()

    # logger.info('creating google account')
    
    # success, email, password = create_google_account(driver, 'Test', 'User')
    # if not success:
    #     logger.error('something went wrong')
    # else:
    #     logger.debug('account created successfully')

    # logger.info('creating instagram account')
    logger.info(get_balance())
    # logger.info(get_active_activation_by_phone_number(''))
