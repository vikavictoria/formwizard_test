import os
import unittest
import time


from python.commom.selenium import Selenium, true

USERS = {
    'successfully': {'username': os.getenv('FA_username'), 'password':os.getenv('FA_password')},
    'failed': {'username': 'Netfon', 'password': 'ADMIN123'},
}


class FormBrowser_login(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = Selenium.launch({'headless': true(os.getenv('HEADLESS', True))})

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_open_browser(self):
        self.driver.get("http://144.76.0.171:88/app/dashboard")
        assert "Form Browser" in self.driver.title

    def login(self, username, password):
        self.driver.get('http://144.76.0.171:88/login')
        self.driver.find_element_by_tag_name('finfire-input').send_keys(username)
        self.driver.find_element_by_tag_name('finfire-input-password').send_keys(password)
        self.driver.find_element_by_tag_name('finfire-button-main').click()

    def test_login_successfully(self):
        self.login(**USERS['successfully'])
        time.sleep(1)
        assert "Interactive Form Files" in self.driver.page_source

    def test_failed_wrong_credentials(self):
        self.login(**USERS['failed'])
        time.sleep(1)
        assert "Bad credentials" in self.driver.page_source

if __name__ == '__main__':
    unittest.main()