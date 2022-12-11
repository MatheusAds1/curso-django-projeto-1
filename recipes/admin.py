from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'is_published']
    list_display_links = ['title', 'created_at']
    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']
    list_filter = ['category', 'author', 'is_published', 'preparation_steps_is_html']
    list_per_page = 10
    list_editable = ['is_published']
    ordering = ['-id']
    prepopulated_fields = {
        'slug': ('title',)
    }