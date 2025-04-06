import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.recipes.models import Recipe, RecipeSaved

class Command(BaseCommand):
    help = 'Seed data for saved recipes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding saved recipes data...')
        
        # Get existing users and recipes
        users = User.objects.all()
        recipes = Recipe.objects.filter(status='published')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found. Please run seed_recipes command first.'))
            return
            
        if not recipes.exists():
            self.stdout.write(self.style.WARNING('No published recipes found. Please run seed_recipes command first.'))
            return
        
        # Create saved recipes
        count = 0
        for user in users:
            # Randomly select 1-3 recipes to save for each user
            recipes_to_save = random.sample(list(recipes), min(random.randint(1, 3), len(recipes)))
            
            for recipe in recipes_to_save:
                saved, created = RecipeSaved.objects.get_or_create(
                    user=user,
                    recipe=recipe
                )
                
                if created:
                    count += 1
                    self.stdout.write(f'Created saved recipe: {recipe.title} for user {user.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} saved recipes')) 