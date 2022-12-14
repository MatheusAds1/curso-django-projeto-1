from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login(self):
        string_password = '123456Aa'
        user = User.objects.create_user(username='my_user', password=string_password)

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário ve a mensagem de login com sucesso e seu nome
        self.assertIn(
            f'You are logged in with {user.username} Click here to logout',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )


    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        self.sleep(2)
