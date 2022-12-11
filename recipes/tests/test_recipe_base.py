from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeMixin():
    def make_category(self, name='Test') -> Category:
        return Category.objects.create(name=name)

    def make_author(
        self,
        username='matheus',
        first_name='Matheus',
        email='matheus@email.com',
        password='123456'
    ):
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password
        )
    
    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Titulo',
        description='Descricao',
        slug='slug-s',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Passos',
        preparation_steps_is_html=False,
        is_published=True
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published
        )

    def make_recipe_in_batch(self, qty=10):
        recipes = []
        for i in range(qty):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}', 
                'author_data': {'username': f'u{i}'}
                }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
