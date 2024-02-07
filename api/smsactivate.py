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


def request_a_number(service: str, country: str, operator: str | None = None) -> (str, str):
    
    if service not in service_codes.keys():
        logger.error(f'invalid service {service}')
        return
    
    if country not in country_codes.keys():
        logger.error(f'invalid country {country}')
        return
    
    country_code = country_codes[country]
    service_code = service_codes[service]


    response = requests.get(f'https://sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={service_code}&operator={operator}&country={country_code}')

    response = response.content.decode('utf-8').split(':')
    activation_id = response[1]
    phone_number = response[2]

    return activation_id, phone_number[-10:]


def activation_status(id: str) -> str:
    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}').content.decode('utf-8')
    return response


def all_active_activations() -> list:
    response = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getActiveActivations').json()

    if response['status'] == 'success':
        return response['activeActivations']
    
    return []


def get_active_activation_by_phone_number(phone: str) -> dict:
    all_activations = all_active_activations()
    current_activation = list(filter(lambda act: act['phoneNumber'] == phone, all_activations))

    if (len(current_activation) == 0):
        logger.error(f'no active activation for phone number {phone}')
        return {}
    
    return current_activation[0]
