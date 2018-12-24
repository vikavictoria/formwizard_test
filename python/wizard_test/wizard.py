import os
import unittest
import time


from python.commom.selenium import Selenium, true


class Formularwisard_login(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = Selenium.launch({'headless': true(os.getenv('HEADLESS', True))})

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_open_wizard(self):
        self.driver.get("http://144.76.0.171:89/app/dashboard")
        assert "Form Wizard" in self.driver.title

    def test_login_successfully(self):

        self.driver.get("http://144.76.0.171:89/login")

        s_username = self.driver.find_element_by_css_selector('input[type="text"]')
        s_username.send_keys("Netfonds")
        s_password = self.driver.find_element_by_css_selector('input[type="password"]')
        s_password.send_keys("OKX70Z4N")
        s_continue = self.driver.find_element_by_css_selector('button[type="submit"]')
        s_continue.click()

        time.sleep(3)


        assert "Interactive PDF Files" in self.driver.page_source

    def test_failed_wrong_credentials(self):

        self.driver.get("http://144.76.0.171:89/login")

        f_username = self.driver.find_element_by_css_selector('input[type="text"]')
        f_username.send_keys("Netfon")
        f_password = self.driver.find_element_by_css_selector('input[type="password"]')
        f_password.send_keys("ADMIN123")
        f_continue = self.driver.find_element_by_css_selector('button[type="submit"]')
        f_continue.click()

        time.sleep(1)
        assert "Bad credentials" in self.driver.page_source


if __name__ == '__main__':
    unittest.main()
