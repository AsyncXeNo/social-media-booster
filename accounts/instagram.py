import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from selenium_utils import WEB_DRIVER_WAIT_TIMEOUT


SIGNUP_URL = 'https://www.instagram.com/accounts/emailsignup/'


def create_instagram_account(driver: webdriver.Chrome, first_name: str, last_name: str, email: str, password: str) -> (bool, str):

    time.sleep(0.40)
    
    try:
        driver.get(SIGNUP_URL)
    except Exception as e:
        logger.error('error while visiting url')
        logger.error(e)
        return False, '',

    if not _fill_information(driver, first_name, last_name, email, password): return False, ''

    if not _birthinfo(driver): return False, ''


def _fill_information(driver: webdriver.Chrome, first_name: str, last_name: str, email: str, password: str) -> bool:

    full_name = f'{first_name.title()} {last_name.title()}'
    username = email.split('@')[0]
    
    try:
        email_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='emailOrPhone']")
            )
        )
        time.sleep(0.40)
        email_field.send_keys(email)
    except Exception as e:
        logger.error('error while setting email')
        logger.error(e)
        return False
    
    try:
        full_name_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='fullName']")
            )
        )
        time.sleep(0.40)
        full_name_field.send_keys(full_name)
    except Exception as e:
        logger.error('error while setting name')
        logger.error(e)
        return False    
    
    try:
        username_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='username']")
            )
        )
        time.sleep(0.40)
        username_field.send_keys(username)
    except Exception as e:
        logger.error('error while setting username')
        logger.error(e)
        return False 
    
    try:
        password_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']")
            )
        )
        time.sleep(0.40)
        password_field.send_keys(username)
    except Exception as e:
        logger.error('error while setting password')
        logger.error(e)
        return False 

    time.sleep(0.40)

    try:
        WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        ).click()
    except Exception as e:
        logger.error('error while clicking on "next" button on the first page')
        logger.error(e)
        return False
    
    return True


def _birthinfo(driver: webdriver.Chrome) -> bool:

    birth_month = random.randrange(12)
    birth_day = random.randrange(28)
    birth_year = random.randrange(20, 40)

    try:
        month_element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "select[title='Month:']")
            )
        )
        month = Select(month_element)
        time.sleep(0.40)
        month.select_by_index(birth_month)
    except Exception as e:
        logger.error('error while setting month')
        logger.error(e)
        return False
    
    try:
        day_element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "select[title='Day:']")
            )
        )
        day = Select(day_element)
        time.sleep(0.40)
        day.select_by_index(birth_day)
    except Exception as e:
        logger.error('error while setting day')
        logger.error(e)
        return False
    
    try:
        year_element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "select[title='Year:']")
            )
        )
        year = Select(year_element)
        time.sleep(0.40)
        year.select_by_index(birth_year)
    except Exception as e:
        logger.error('error while setting year')
        logger.error(e)
        return False
    
    time.sleep(0.40)

    try:
        WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Next']")
            )
        ).click()
    except Exception as e:
        logger.error('error while clicking "next" button on the birthinfo page')

    return True


def _email_verification(driver: webdriver.Chrome, email: str) -> bool:

    # input[placeholder='Confirmation code']
    # //div[normalize-space()='Next']

    pass
        