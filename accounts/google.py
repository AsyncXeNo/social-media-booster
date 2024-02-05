import time
import datetime
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from selenium_utils import WEB_DRIVER_WAIT_TIMEOUT


SIGNUP_URL = 'https://accounts.google.com/signup'


def create_google_account(driver: webdriver.Chrome, first_name: str, last_name: str) -> (bool, str, str):

    time.sleep(0.40)
    
    try:
        driver.get(SIGNUP_URL)
    except Exception as e:
        logger.error('error while visiting url')
        logger.error(e)
        return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''
    
    if not _name(driver, first_name, last_name): return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''

    if not _birthinfo(driver): return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''

    success, email = _username(driver, first_name, last_name)
    if not success: return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''

    success, password = _password(driver)
    if not success: return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''

    # PHONE NUMBER
    if (_check_for_phone_number(driver)):
        if not _phone_number(driver): return False, '', ''

    if (_check_for_recaptcha(driver)):
        if not _solve_recaptcha(driver): return False, '', ''

    if not _final_steps(driver): return False, '', ''

    return True, email, password


def _check_for_recaptcha(driver: webdriver.Chrome) -> bool:
    #TODO: implement
    return False


def _solve_recaptcha(driver: webdriver.Chrome) -> bool:
    #TODO: implement
    return True


def _name(driver: webdriver.Chrome, first_name: str, last_name: str) -> bool:

    try:
        first_name_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#firstName')
            )
        )
        time.sleep(0.40)
        first_name_field.send_keys(first_name)
    except Exception as e:
        logger.error('error while entering first name')
        logger.error(e)
        return False
    
    try:
        last_name_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#lastName')
            )
        )
        time.sleep(0.40)
        last_name_field.send_keys(last_name)
    except Exception as e:
        logger.error('error while entering last name')
        logger.error(e)
        return False

    try:
        next_button = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[type='button']")
            )
        )
        time.sleep(0.40)
        next_button.click()
    except Exception as e:
        logger.error('error while clicking "next" on the name page')
        logger.error(e)
        return False
    
    return True


def _birthinfo(driver: webdriver.Chrome) -> bool:
    
    current_year = datetime.datetime.now().year
    birth_day = random.randint(1, 28)
    birth_month = random.randrange(12)
    birth_year = random.randint(current_year - 40, current_year - 20)
    gender_index = random.randrange(2)

    try:
        month_element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#month")
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
        day = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#day")
            )
        )
        time.sleep(0.40)
        day.send_keys(birth_day)
    except Exception as e:
        logger.error('error while setting day')
        logger.error(e)
        return False

    try:
        year = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#year")
            )
        )
        time.sleep(0.40)
        year.send_keys(birth_year)
    except Exception as e:
        logger.error('error while setting year')
        logger.error(e)
        return False

    try:
        gender_element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#gender")
            )
        )
        gender = Select(gender_element)
        time.sleep(0.40)
        gender.select_by_index(gender_index)
    except Exception as e:
        logger.error('error while setting gender')
        logger.error(e)
        return False

    try:
        next_button = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[type='button']")
            )
        )
        time.sleep(0.40)
        next_button.click()
    except Exception as e:
        logger.error('error while clicking "next" on the birthinfo page')
        logger.error(e)
        return False

    return True
    

def _username(driver: webdriver.Chrome, first_name: str, last_name: str) -> (bool, str):
    suffix = random.randint(100000, 999999)
    username = f'{first_name.lower()}.{last_name.lower()}{suffix}'

    try:
        name_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='Username']")
            )
        )
        time.sleep(0.40)
        name_field.send_keys(username)
    except Exception as e:
        logger.error('error while setting username')
        logger.error(e)
        return False, ''

    try:
        next_button = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.TAG_NAME, 'button')
            )
        )
        time.sleep(0.40)
        next_button.click()
    except Exception as e:
        logger.error('error while clicking "next" on the username page')
        logger.error(e)
        return False, ''
    
    return True, username+'@gmail.com'


def _password(driver: webdriver.Chrome) -> bool:
    password = f'{"".join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))}_{random.randint(10000, 99999)}'

    try:
        password_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='Passwd']")
            )
        )
        time.sleep(0.40)
        password_field.send_keys(password)
    except Exception as e:
        logger.error('error while setting password')
        logger.error(e)
        return False, ''
    
    try:
        password_field = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='PasswdAgain']")
            )
        )
        time.sleep(0.40)
        password_field.send_keys(password)
    except Exception as e:
        logger.error('error while setting confirm password')
        logger.error(e)
        return False, ''
    
    try:
        next_button = WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.TAG_NAME, 'button')
            )
        )
        time.sleep(0.40)
        next_button.click()
    except Exception as e:
        logger.error('error while clicking "next" on the password page')
        logger.error(e)
        return False, ''
    
    return True, password
    

def _check_for_phone_number(driver) -> bool:
    
    try:
        WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#phoneNumberId')
            )
        )
        return True
    except:
        return False


def _phone_number(driver) -> bool:
    
    return True


def _final_steps(driver) -> bool:
    
    return True