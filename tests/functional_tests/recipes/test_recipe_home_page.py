from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)


    @patch('recipes.views.PER_PAGE', new=6)
    def test_recipe_search_input_can_find_correct_recipes(self):
        # Make recipes
        recipes = self.make_recipe_in_batch()


        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Ve um campo de busca com a mensagem "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca "Recipe title 1" para encontrar a receita com esse título
        search_input.click()
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # O usuário ve o que estava pesquisando
        self.assertIn(
            recipes[0].title,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )


    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        # Make recipes
        recipes = self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Ve que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        # Ve que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
