import unittest

from selenium.webdriver.common.by import By

from webutils import browser


class DriverTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = browser.get_driver(browser_id='chrome',
            headless=False)

    def tearDown(self):
        self.driver.quit()

    def test_element(self):
        url = 'https://1337x.to/search/sfsfsfsdfsd/1/'
        self.driver.get(url)
        el = self.driver.find_element(By.XPATH,
            '//p[contains(text(), "No results were returned.")]')
        print(el)
        self.assertTrue(el)