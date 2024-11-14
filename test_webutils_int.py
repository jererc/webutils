import unittest

from selenium.webdriver.common.by import By

import webutils


class BrowserTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webutils.Browser(browser_id='chrome', headless=False)
        self.driver = self.browser.driver

    def tearDown(self):
        self.driver.quit()

    def test_no_result(self):
        url = 'https://1337x.to/search/sfsfsfsdfsd/1/'
        self.driver.get(url)
        el = self.driver.find_element(By.XPATH,
            "//p[contains(text(), 'No results were returned.')]")
        print(el)
        self.assertTrue(el)
