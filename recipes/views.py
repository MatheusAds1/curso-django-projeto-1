from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.db.models import Q, F, Value
from recipes.models import Recipe
from utils.recipes.pagination import make_pagination
import os
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count, Sum, Avg
from django.db.models.functions import Concat

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def theory(request, *args, **kwargs):
    # try:
    #     recipes = Recipe.objects.get(pk=10000)
    # except ObjectDoesNotExist:
    #     recipes = None

    # recipes = Recipe.objects.filter(
    #     Q(
    #         title__icontains='da',
    #         id__gt=2,
    #         is_published=True,) |
    #     Q(
    #         id__gt=10000
    #     )
    # )

    # recipes = Recipe.objects.filter(
    #     id=F('author__id'),
    # )[:10]

    # recipes = Recipe.objects.values('id', 'title')
    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')')
        )
    )
    number_of_recipes = recipes.aggregate(number=Count('id'))
    
    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by: int = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name: str = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        ctx.update({ 'recipes': page_obj, 'pagination_range': pagination_range })
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name: str = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name: str = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):

        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name: str = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name: str = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{ search_term }" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name: str = 'recipe'
    template_name: str = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        
        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''
        
        del(recipe_dict['is_published'])

        return JsonResponse(
            recipe_dict,
            safe=False
        )


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })


def category(request, category_id):
    # recipe = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    #
    # if not recipe:
    #     raise Http404('Not found')
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category'
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).filter(is_published=True).order_by('-id')

    print(recipes.query)

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{ search_term }" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
