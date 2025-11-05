from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from time import sleep

class OrderPage(BasePage):
    FIELDS = [
        (By.ID, "field1"),
        (By.ID, "field2"),
        (By.ID, "field3"),
        (By.ID, "field4"),
        (By.ID, "field5"),
    ]
    SUBMIT = (By.ID, "submitBtn")
    SUCCESS = (By.ID, "success")
    ERROR = (By.ID, "error")

    def fill_form(self, values, delay_per_field=1):
        for locator, value in zip(self.FIELDS, values):
            self.type(locator, value, delay=0.2)
            sleep(delay_per_field)

    def submit_form(self):
        self.click(self.SUBMIT)

    def get_success_message(self):
        return self.find(self.SUCCESS).text

    def get_error_message(self):
        return self.find(self.ERROR).text
