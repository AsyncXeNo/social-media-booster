import os
import shutil
import datetime
import threading

import pandas
from loguru import logger


ACCOUNT_FILE_PATH = 'data/accounts.csv'


empty = {
    'email': [],
    'password': [],
    'phone': [],
    'instagram': [],
    'facebook': [],
    'facebook_verified': []
}

lock = threading.Lock()


def _acquire_lock(func):
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


@_acquire_lock
def backup() -> None:
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copy2(ACCOUNT_FILE_PATH, f'data/accounts_backup_{current_datetime}.csv')


@_acquire_lock
def create_fresh_file() -> None:
    df = pandas.DataFrame(data=empty)
    df.to_csv(ACCOUNT_FILE_PATH)


@_acquire_lock
def add_account(email: str, password: str, phone: str, instagram: str, facebook: str, facebook_verified: bool) -> bool:
    existing_accounts = get_existing_accounts()

    if email in existing_accounts['email'].values:
        logger.error(f'account with email {email} already exists, cannot add duplicate accounts')
        return False

    new_account = {
        'email': email,
        'password': password,
        'phone': phone,
        'instagram': instagram,
        'facebook': facebook,
        'facebook_verified': facebook_verified
    }

    existing_accounts = existing_accounts.append(new_account, ignore_index=True)

    existing_accounts.to_csv(ACCOUNT_FILE_PATH, index=False)

    return True


@_acquire_lock
def get_existing_accounts() -> pandas.DataFrame:
    if not(os.path.exists(ACCOUNT_FILE_PATH)):
        logger.warning('no existing accounts, creating a fresh file')
        create_fresh_file()
    return pandas.read_csv(ACCOUNT_FILE_PATH, index_col=0)


@_acquire_lock
def get_random_account() -> dict:
    existing_accounts = get_existing_accounts()
    if existing_accounts.empty:
        return None
    random_account = existing_accounts.sample().to_dict(orient='records')
    return random_account[0]


@_acquire_lock
def get_account_by_email(email: str) -> dict:
    existing_accounts = get_existing_accounts()
    account = existing_accounts[existing_accounts['email'] == email].to_dict(orient='records')
    return account[0] if account else None


@_acquire_lock
def delete_account_by_email(email: str) -> None:
    logger.warning(f'permanently deleting account with email {email}')
    existing_accounts = get_existing_accounts()
    existing_accounts = existing_accounts[existing_accounts['email'] != email]
    existing_accounts.to_csv(ACCOUNT_FILE_PATH, index=False)