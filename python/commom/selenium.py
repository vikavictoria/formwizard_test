from selenium import webdriver
from selenium.common.exceptions import WebDriverException


PARAMS = {
    'chromedriver': '/usr/bin/chromedriver',
    'user_agent': 'chrome',
    'headless': 'true',
    'incognito': 'false',
    'wait_duration': 60,  # seconds
    'proxy_server': '',  # host:port - no basic auth support
    'download_dir': '',
    'lang': 'en',
}

USER_AGENTS = {
    'chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+'
    ' (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'ie7': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727;'
    ' Media Center PC 5.0; .NET CLR 3.0.04506)',
    'firefox': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
}


class Selenium:

    @staticmethod
    def launch(params=None):
        params = {**PARAMS, **(params or {})}

        # options
        options = webdriver.ChromeOptions()
        if params.get('download_dir'):
            experimental = {
                'download.default_directory': params.get('download_dir'),
                'download.prompt_for_download': False,
                'directory_upgrade': True,
                'safebrowsing.enabled': True,
            }
            options.add_experimental_option('prefs', experimental)
        if params.get('user_agent'):
            params['user_agent'] = USER_AGENTS.get(params.get('user_agent'))
            options.add_argument('--user-agent=%s' % params.get('user_agent'))
        if params.get('proxy_server'):
            options.add_argument('--proxy-server=%s' % params.get('proxy_server'))
        if true(params.get('headless')):
            options.add_argument('--headless')
        if true(params.get('incognito')):
            options.add_argument("--incognito")
        options.add_argument('--lang=%s' % params.get('lang'))
        options.add_argument('window-size=3840x2160')

        # driver
        service_args = ['--verbose', '--log-path=/dev/null']  # workaround
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        driver = webdriver.Chrome(
            executable_path=params.get('chromedriver'),
            options=options,
            service_args=service_args,
            desired_capabilities=capabilities)
        setattr(driver, '_wait_duration', int(params.get('wait_duration')))
        driver.implicitly_wait(driver._wait_duration)
        driver.set_script_timeout(driver._wait_duration)
        try:
            driver.maximize_window()
        except WebDriverException:
            pass  # ok if not available
        return driver

    @staticmethod
    def quit(driver):
        try:
            driver.quit()
        except Exception:
            pass


def true(val):
    return val if isinstance(val, bool) else str(val).lower() in ('1', 'true', 'on')
