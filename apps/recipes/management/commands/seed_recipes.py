from apps.recipes.seeders import Command as RecipeSeeder

class Command(RecipeSeeder):
    help = 'Seed recipe data including categories, ingredients, and instructions' 