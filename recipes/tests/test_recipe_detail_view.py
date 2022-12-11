from django.urls import reverse, resolve
from recipes.tests.test_recipe_base import RecipeTestBase
from unittest import skip
from recipes import views


class RecipeDetailViewTest(RecipeTestBase):
    @skip('Skip')
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        self.fail('Testando o self.fail')

    def test_recipe_detail_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 20})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipe(self):
        title = 'Detail test'
        self.make_recipe(title=title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipe']

        self.assertIn(title, content)
