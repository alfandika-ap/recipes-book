from django.contrib import admin
from .models import Recipe, Ingredient, Instruction, Category

# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
  list_display = ('title', 'created_by', 'created_at', 'updated_at')
  search_fields = ('title', 'created_by__username')
  list_filter = ('created_by', 'created_at', 'updated_at')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
  list_display = ('name', 'quantity', 'recipe')
  search_fields = ('name', 'recipe__title')
  list_filter = ('recipe__title',)

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
  list_display = ('number', 'description', 'recipe')
  search_fields = ('description', 'recipe__title')
  list_filter = ('recipe__title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')
  search_fields = ('name',)
  list_filter = ('name',)