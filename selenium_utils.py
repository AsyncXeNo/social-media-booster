import zipfile

from selenium import webdriver
from fake_useragent import UserAgent


WEB_DRIVER_WAIT_TIMEOUT = 10


def _driver_wrapper(f):
    def wrapper(*args, **kwargs):
        driver: webdriver.Chrome = f(*args, **kwargs)

        driver.maximize_window()
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        return driver
    
    return wrapper


def _get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    ua = UserAgent()

    chrome_options.add_argument(f'--user-agent={ua.random}')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option("useAutomationExtension", False) 

    return chrome_options


@_driver_wrapper
def get_chromedriver_without_proxy() -> webdriver.Chrome:
    chrome_options = _get_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


@_driver_wrapper
def get_chromedriver_with_proxy(host: str, port: str, user: str, password: str) -> webdriver.Chrome:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (host, port, user, password)

    chrome_options = _get_chrome_options()

    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)

    chrome_options.add_extension(pluginfile)

    driver = webdriver.Chrome(options=chrome_options)

    return driver
