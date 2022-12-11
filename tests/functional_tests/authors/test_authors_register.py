from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
        
        form.find_element(By.NAME, 'email').send_keys('matheus@email.com')


    def get_form(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )


    def form_field_test_with_callback(self, callback):
        form = self.get_form()
        self.fill_form_dummy_data(form)

        callback(form)
        return form


    def test_first_name_field_empty_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Your first name')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('Write your first name', form.text)

        self.form_field_test_with_callback(callback)


    def test_last_name_field_empty_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your last name')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('Write your last name', form.text)

        self.form_field_test_with_callback(callback)


    def test_user_valid_data_register_successfully(self):
        form = self.get_form()

        self.get_by_placeholder(form, 'Your first name').send_keys('First name')
        self.get_by_placeholder(form, 'Your last name').send_keys('Last name')
        self.get_by_placeholder(form, 'Your username').send_keys('Username')
        self.get_by_placeholder(form, 'Your email').send_keys('email@email.com')
        self.get_by_placeholder(form, 'Your password').send_keys('123456Aa')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('123456Aa')

        form.submit()

        self.assertIn(
            'Your user was created, please log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
