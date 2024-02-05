import requests
from loguru import logger

from env import get_var


api_key = get_var('SMS_ACTIVATE_API_KEY')

service_codes = {
    'google': 'go',
    'facebook': 'fb',
    'instagram': 'ig'
}

country_codes = {
    'Indonesia': 6,
    'England': 16,
    'Philippines': 4,
    'Colombia': 33,
    'Thailand': 52,
    'Chile': 151,
    'Brazil': 73,
    'Malaysia': 7,
    'SouthAfrica': 31
}


def get_balance() -> float:
    """
    Returns the balance in RUB
    """

    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getBalance').content.decode('utf8')
    return float(response.split(':')[-1])


def get_top_countries(service: str) -> dict:

    if service not in service_codes.keys():
        logger.error(f'invalid service {service}')
        return
    
    code = service_codes[service]
    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getTopCountriesByService&service={code}').json()
    sliced = [ response[key] for key in list(response.keys())[:10] ]
    return sliced


def get_operators(country: str) -> dict:

    if country not in country_codes.keys():
        logger.error(f'invalid country {country}')
        return

    country_code = country_codes[country]
    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getOperators&country={country_code}').json()

    if response.get('status') != 'success':
        logger.error(f'something went wrong while getting operators, status: {response.get("status")}')
    
    return response.get('countryOperators')[str(country_code)]


def get_available_quantity_of_numbers(country: str, operator: str, service: str) -> int:

    if country not in country_codes.keys():
        logger.error(f'invalid country {country}')
        return
    
    if service not in service_codes.keys():
        logger.error(f'invalid service {service}')
        return

    service_code = service_codes[service]
    country_code = country_codes[country]
    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getNumbersStatus&country={country_code}&operator={operator}').json()

    return response[f'{service_code}_0']
