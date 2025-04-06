import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.recipes.models import Category, Recipe, Ingredient, Instruction, STATUS_CHOICES

class Command(BaseCommand):
    help = 'Seed data for recipes app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create categories
        categories = self._create_categories()
        
        # Create recipes with ingredients and instructions
        self._create_recipes(categories)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
    
    def _create_categories(self):
        category_data = [
            {'name': 'Breakfast', 'description': 'Start your day with these delicious breakfast recipes'},
            {'name': 'Lunch', 'description': 'Perfect meals for your midday break'},
            {'name': 'Dinner', 'description': 'End your day with these fulfilling dinner recipes'},
            {'name': 'Dessert', 'description': 'Sweet treats for any time of day'},
            {'name': 'Appetizer', 'description': 'Start your meal with these tasty bites'},
            {'name': 'Soup', 'description': 'Warm up with these comforting soup recipes'},
            {'name': 'Salad', 'description': 'Fresh and healthy salad recipes'},
            {'name': 'Vegetarian', 'description': 'Delicious meat-free recipes'},
            {'name': 'Vegan', 'description': 'Plant-based recipes for everyone'},
            {'name': 'Gluten-Free', 'description': 'Recipes without gluten'},
        ]
        
        categories = []
        for data in category_data:
            category, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            categories.append(category)
            
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories
    
    def _create_recipes(self, categories):
        # Make sure we have at least one user
        user, created = User.objects.get_or_create(
            username='adminrecipe',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('adminrecipe')
            user.save()
            self.stdout.write(f'Created user: {user.username}')
        
        recipe_data = [
            {
                'title': 'Fluffy Pancakes',
                'description': 'Delicious homemade pancakes that are light and fluffy',
                'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445',
                'rating': 4.8,
                'total_time': 30,
                'status': 'published',
                'category': 'Breakfast',
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': '2 cups'},
                    {'name': 'Baking powder', 'quantity': '2 teaspoons'},
                    {'name': 'Sugar', 'quantity': '2 tablespoons'},
                    {'name': 'Salt', 'quantity': '1/2 teaspoon'},
                    {'name': 'Milk', 'quantity': '1 1/2 cups'},
                    {'name': 'Eggs', 'quantity': '2'},
                    {'name': 'Vanilla extract', 'quantity': '1 teaspoon'},
                    {'name': 'Butter', 'quantity': '3 tablespoons, melted'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large bowl, sift together the flour, baking powder, sugar and salt.'},
                    {'number': 2, 'description': 'Make a well in the center and pour in the milk, eggs and melted butter; mix until smooth.'},
                    {'number': 3, 'description': 'Heat a lightly oiled griddle or frying pan over medium-high heat.'},
                    {'number': 4, 'description': 'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake. Brown on both sides and serve hot.'},
                ]
            },
            {
                'title': 'Classic Caesar Salad',
                'description': 'A classic Caesar salad with homemade dressing',
                'image_url': 'https://images.unsplash.com/photo-1551248429-40975aa4de74',
                'rating': 4.5,
                'total_time': 20,
                'status': 'published',
                'category': 'Salad',
                'ingredients': [
                    {'name': 'Romaine lettuce', 'quantity': '1 head, chopped'},
                    {'name': 'Croutons', 'quantity': '1 cup'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2 cup, grated'},
                    {'name': 'Garlic', 'quantity': '2 cloves, minced'},
                    {'name': 'Lemon juice', 'quantity': '2 tablespoons'},
                    {'name': 'Olive oil', 'quantity': '1/3 cup'},
                    {'name': 'Dijon mustard', 'quantity': '1 teaspoon'},
                    {'name': 'Anchovy paste', 'quantity': '1 teaspoon'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a bowl, whisk together the garlic, lemon juice, olive oil, mustard, and anchovy paste.'},
                    {'number': 2, 'description': 'In a large bowl, combine the lettuce, croutons, and Parmesan cheese.'},
                    {'number': 3, 'description': 'Pour the dressing over the salad and toss to coat evenly.'},
                    {'number': 4, 'description': 'Serve immediately.'},
                ]
            },
            {
                'title': 'Chocolate Lava Cake',
                'description': 'Decadent chocolate cakes with a molten center',
                'image_url': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb',
                'rating': 4.9,
                'total_time': 25,
                'status': 'published',
                'category': 'Dessert',
                'ingredients': [
                    {'name': 'Butter', 'quantity': '1/2 cup'},
                    {'name': 'Semisweet chocolate', 'quantity': '4 ounces, chopped'},
                    {'name': 'Eggs', 'quantity': '2'},
                    {'name': 'Egg yolks', 'quantity': '2'},
                    {'name': 'Sugar', 'quantity': '1/4 cup'},
                    {'name': 'Vanilla extract', 'quantity': '1 teaspoon'},
                    {'name': 'All-purpose flour', 'quantity': '2 tablespoons'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Preheat oven to 425°F. Butter and flour four 6-ounce ramekins.'},
                    {'number': 2, 'description': 'In a double boiler, melt butter and chocolate together.'},
                    {'number': 3, 'description': 'In a mixing bowl, beat eggs, egg yolks, sugar, and vanilla until light and thick.'},
                    {'number': 4, 'description': 'Fold in the melted chocolate mixture, then gently fold in the flour.'},
                    {'number': 5, 'description': 'Divide the batter among the ramekins and bake for 12-14 minutes.'},
                    {'number': 6, 'description': 'Let stand for 1 minute, then run a knife around the edges and invert onto plates.'},
                ]
            },
            {
                'title': 'Spaghetti Carbonara',
                'description': 'Classic Italian pasta dish with eggs, cheese, and pancetta',
                'image_url': 'https://images.unsplash.com/photo-1588013273468-315fd88ea34c',
                'rating': 4.7,
                'total_time': 30,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'Spaghetti', 'quantity': '1 pound'},
                    {'name': 'Pancetta or bacon', 'quantity': '8 ounces, diced'},
                    {'name': 'Garlic', 'quantity': '3 cloves, minced'},
                    {'name': 'Eggs', 'quantity': '4 large'},
                    {'name': 'Parmesan cheese', 'quantity': '1 cup, grated'},
                    {'name': 'Black pepper', 'quantity': '1 teaspoon, freshly ground'},
                    {'name': 'Salt', 'quantity': 'To taste'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Cook spaghetti in a large pot of salted boiling water until al dente.'},
                    {'number': 2, 'description': 'Meanwhile, in a large skillet, cook the pancetta over medium heat until crispy.'},
                    {'number': 3, 'description': 'Add garlic to the skillet and cook for 30 seconds.'},
                    {'number': 4, 'description': 'In a bowl, whisk together eggs, cheese, and pepper.'},
                    {'number': 5, 'description': 'Drain pasta, reserving 1/2 cup of pasta water.'},
                    {'number': 6, 'description': 'Add hot pasta to the skillet with pancetta and toss quickly.'},
                    {'number': 7, 'description': 'Remove from heat, add egg mixture and toss until creamy. Add pasta water if needed.'},
                    {'number': 8, 'description': 'Serve immediately with extra cheese and pepper.'},
                ]
            },
            {
                'title': 'Vegetable Stir Fry',
                'description': 'Quick and healthy vegetable stir fry with a savory sauce',
                'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'rating': 4.3,
                'total_time': 25,
                'status': 'published',
                'category': 'Vegetarian',
                'ingredients': [
                    {'name': 'Broccoli', 'quantity': '2 cups, florets'},
                    {'name': 'Bell peppers', 'quantity': '2, sliced'},
                    {'name': 'Carrots', 'quantity': '2, julienned'},
                    {'name': 'Snow peas', 'quantity': '1 cup'},
                    {'name': 'Garlic', 'quantity': '3 cloves, minced'},
                    {'name': 'Ginger', 'quantity': '1 tablespoon, minced'},
                    {'name': 'Soy sauce', 'quantity': '3 tablespoons'},
                    {'name': 'Sesame oil', 'quantity': '1 tablespoon'},
                    {'name': 'Vegetable oil', 'quantity': '2 tablespoons'},
                    {'name': 'Cornstarch', 'quantity': '1 teaspoon'},
                    {'name': 'Water', 'quantity': '1/4 cup'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a small bowl, mix soy sauce, water, and cornstarch.'},
                    {'number': 2, 'description': 'Heat vegetable oil in a wok or large skillet over high heat.'},
                    {'number': 3, 'description': 'Add garlic and ginger, stir fry for 30 seconds.'},
                    {'number': 4, 'description': 'Add vegetables and stir fry for 5-7 minutes until crisp-tender.'},
                    {'number': 5, 'description': 'Pour in sauce mixture and cook until thickened, about 1 minute.'},
                    {'number': 6, 'description': 'Drizzle with sesame oil and serve over rice.'},
                ]
            },
            {
                'title': 'Nasi Goreng',
                'description': 'Indonesian fried rice with savory flavors and aromatic spices',
                'image_url': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'rating': 4.8,
                'total_time': 25,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'Cooked white rice', 'quantity': '3 cups, cold'},
                    {'name': 'Chicken', 'quantity': '200g, diced'},
                    {'name': 'Shallots', 'quantity': '4, thinly sliced'},
                    {'name': 'Garlic', 'quantity': '3 cloves, minced'},
                    {'name': 'Red chili', 'quantity': '2, sliced'},
                    {'name': 'Sweet soy sauce (kecap manis)', 'quantity': '2 tablespoons'},
                    {'name': 'Vegetable oil', 'quantity': '2 tablespoons'},
                    {'name': 'Eggs', 'quantity': '2'},
                    {'name': 'Spring onions', 'quantity': '2, chopped'},
                    {'name': 'Cucumber', 'quantity': '1, sliced for garnish'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Heat oil in a wok over high heat.'},
                    {'number': 2, 'description': 'Add shallots, garlic, and chili. Stir-fry until fragrant.'},
                    {'number': 3, 'description': 'Add diced chicken and cook until no longer pink.'},
                    {'number': 4, 'description': 'Push everything to one side of the wok and crack eggs into the empty space. Scramble until set.'},
                    {'number': 5, 'description': 'Add cold rice and break up any clumps.'},
                    {'number': 6, 'description': 'Pour sweet soy sauce over rice and stir to evenly distribute.'},
                    {'number': 7, 'description': 'Cook for 3-4 minutes until rice is heated through and slightly crispy.'},
                    {'number': 8, 'description': 'Add spring onions, stir once more, and serve with cucumber slices.'},
                ]
            },
            {
                'title': 'Avocado Toast',
                'description': 'Simple and nutritious breakfast with creamy avocado on toasted bread',
                'image_url': 'https://images.unsplash.com/photo-1588137378633-dea1336ce1e2',
                'rating': 4.5,
                'total_time': 10,
                'status': 'published',
                'category': 'Breakfast',
                'ingredients': [
                    {'name': 'Ripe avocados', 'quantity': '2'},
                    {'name': 'Whole grain bread', 'quantity': '4 slices'},
                    {'name': 'Lemon juice', 'quantity': '1 tablespoon'},
                    {'name': 'Red pepper flakes', 'quantity': '1/2 teaspoon'},
                    {'name': 'Salt', 'quantity': 'To taste'},
                    {'name': 'Black pepper', 'quantity': 'To taste'},
                    {'name': 'Cherry tomatoes', 'quantity': '1/2 cup, halved (optional)'},
                    {'name': 'Feta cheese', 'quantity': '1/4 cup, crumbled (optional)'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Toast the bread slices until golden and crisp.'},
                    {'number': 2, 'description': 'Cut avocados in half, remove the pit, and scoop the flesh into a bowl.'},
                    {'number': 3, 'description': 'Add lemon juice, salt, and pepper to the avocado and mash to desired consistency.'},
                    {'number': 4, 'description': 'Spread the avocado mixture on the toast.'},
                    {'number': 5, 'description': 'Sprinkle with red pepper flakes.'},
                    {'number': 6, 'description': 'Top with cherry tomatoes and feta cheese if using.'},
                ]
            },
            {
                'title': 'Mango Sticky Rice',
                'description': 'Thai dessert with sweet coconut sticky rice and fresh mango',
                'image_url': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7',
                'rating': 4.9,
                'total_time': 45,
                'status': 'published',
                'category': 'Dessert',
                'ingredients': [
                    {'name': 'Glutinous rice', 'quantity': '1 cup'},
                    {'name': 'Coconut milk', 'quantity': '1 1/2 cups'},
                    {'name': 'Sugar', 'quantity': '1/4 cup'},
                    {'name': 'Salt', 'quantity': '1/4 teaspoon'},
                    {'name': 'Ripe mangoes', 'quantity': '2, peeled and sliced'},
                    {'name': 'Toasted sesame seeds', 'quantity': '1 tablespoon for garnish'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Soak the glutinous rice in water for at least 3 hours or overnight.'},
                    {'number': 2, 'description': 'Drain the rice and rinse under cold water.'},
                    {'number': 3, 'description': 'Steam the rice for 25-30 minutes until cooked and sticky.'},
                    {'number': 4, 'description': 'While the rice is cooking, heat 1 cup of coconut milk with sugar and salt in a saucepan until sugar dissolves.'},
                    {'number': 5, 'description': 'When rice is done, transfer to a bowl and pour the coconut milk mixture over it.'},
                    {'number': 6, 'description': 'Cover and let sit for 15 minutes to absorb the liquid.'},
                    {'number': 7, 'description': 'For the sauce, heat the remaining 1/2 cup coconut milk in a small saucepan until it thickens slightly.'},
                    {'number': 8, 'description': 'Serve the sticky rice with mango slices, drizzle with coconut sauce, and sprinkle with toasted sesame seeds.'},
                ]
            },
            {
                'title': 'Mushroom Risotto',
                'description': 'Creamy Italian rice dish with earthy mushrooms and Parmesan cheese',
                'image_url': 'https://images.unsplash.com/photo-1548943487-a2e4e43b4853',
                'rating': 4.7,
                'total_time': 40,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'Arborio rice', 'quantity': '1 1/2 cups'},
                    {'name': 'Mixed mushrooms', 'quantity': '300g, sliced'},
                    {'name': 'Vegetable broth', 'quantity': '4 cups, warm'},
                    {'name': 'White wine', 'quantity': '1/2 cup'},
                    {'name': 'Shallots', 'quantity': '2, finely chopped'},
                    {'name': 'Garlic', 'quantity': '2 cloves, minced'},
                    {'name': 'Butter', 'quantity': '2 tablespoons'},
                    {'name': 'Olive oil', 'quantity': '2 tablespoons'},
                    {'name': 'Parmesan cheese', 'quantity': '1/2 cup, grated'},
                    {'name': 'Fresh thyme', 'quantity': '1 tablespoon, chopped'},
                    {'name': 'Salt and pepper', 'quantity': 'To taste'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large pan, heat 1 tablespoon of olive oil and cook mushrooms until golden. Remove and set aside.'},
                    {'number': 2, 'description': 'In the same pan, heat the remaining olive oil and butter.'},
                    {'number': 3, 'description': 'Add shallots and cook until soft, then add garlic and cook for 30 seconds.'},
                    {'number': 4, 'description': 'Add rice and stir to coat in the oil and butter. Toast for 1-2 minutes.'},
                    {'number': 5, 'description': 'Add wine and stir until absorbed.'},
                    {'number': 6, 'description': 'Add warm broth one ladleful at a time, waiting until each addition is absorbed before adding more.'},
                    {'number': 7, 'description': 'Stir constantly, cooking for about 18-20 minutes until rice is creamy and al dente.'},
                    {'number': 8, 'description': 'Stir in the cooked mushrooms, Parmesan cheese, and thyme.'},
                    {'number': 9, 'description': 'Season with salt and pepper and serve hot.'},
                ]
            },
            {
                'title': 'Chicken Shawarma',
                'description': 'Middle Eastern spiced chicken with warm pita and tahini sauce',
                'image_url': 'https://images.unsplash.com/photo-1606674727310-6d55b6960d8f',
                'rating': 4.6,
                'total_time': 50,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'Chicken thighs', 'quantity': '1 kg, boneless, skinless'},
                    {'name': 'Plain yogurt', 'quantity': '1/2 cup'},
                    {'name': 'Lemon juice', 'quantity': '2 tablespoons'},
                    {'name': 'Olive oil', 'quantity': '3 tablespoons'},
                    {'name': 'Garlic', 'quantity': '4 cloves, minced'},
                    {'name': 'Cumin', 'quantity': '2 teaspoons'},
                    {'name': 'Paprika', 'quantity': '2 teaspoons'},
                    {'name': 'Turmeric', 'quantity': '1 teaspoon'},
                    {'name': 'Cinnamon', 'quantity': '1/2 teaspoon'},
                    {'name': 'Cayenne pepper', 'quantity': '1/4 teaspoon'},
                    {'name': 'Salt', 'quantity': '1 1/2 teaspoons'},
                    {'name': 'Black pepper', 'quantity': '1/2 teaspoon'},
                    {'name': 'Pita bread', 'quantity': '6'},
                    {'name': 'Tahini sauce', 'quantity': '1/2 cup'},
                    {'name': 'Sliced cucumber', 'quantity': '1 cup'},
                    {'name': 'Sliced tomatoes', 'quantity': '1 cup'},
                    {'name': 'Red onion', 'quantity': '1, thinly sliced'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large bowl, combine yogurt, lemon juice, olive oil, garlic, and all the spices.'},
                    {'number': 2, 'description': 'Add chicken thighs and toss to coat thoroughly.'},
                    {'number': 3, 'description': 'Cover and refrigerate for at least 2 hours, preferably overnight.'},
                    {'number': 4, 'description': 'Preheat oven to 425°F (220°C).'},
                    {'number': 5, 'description': 'Arrange marinated chicken on a baking sheet.'},
                    {'number': 6, 'description': 'Bake for 30-35 minutes until chicken is golden and cooked through.'},
                    {'number': 7, 'description': 'Let rest for 5 minutes, then slice into strips.'},
                    {'number': 8, 'description': 'Warm pita bread in the oven for 2-3 minutes.'},
                    {'number': 9, 'description': 'Serve chicken in pita with tahini sauce, cucumber, tomatoes, and red onion.'},
                ]
            },
            {
                'title': 'Vegan Buddha Bowl',
                'description': 'Nutritious bowl with roasted vegetables, grains, and tahini dressing',
                'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'rating': 4.5,
                'total_time': 35,
                'status': 'published',
                'category': 'Vegan',
                'ingredients': [
                    {'name': 'Quinoa', 'quantity': '1 cup, uncooked'},
                    {'name': 'Sweet potato', 'quantity': '1 large, cubed'},
                    {'name': 'Chickpeas', 'quantity': '1 can (15 oz), drained and rinsed'},
                    {'name': 'Broccoli', 'quantity': '1 head, cut into florets'},
                    {'name': 'Avocado', 'quantity': '1, sliced'},
                    {'name': 'Cherry tomatoes', 'quantity': '1 cup, halved'},
                    {'name': 'Cucumber', 'quantity': '1/2, sliced'},
                    {'name': 'Red cabbage', 'quantity': '1 cup, shredded'},
                    {'name': 'Olive oil', 'quantity': '2 tablespoons'},
                    {'name': 'Cumin', 'quantity': '1 teaspoon'},
                    {'name': 'Paprika', 'quantity': '1 teaspoon'},
                    {'name': 'Salt and pepper', 'quantity': 'To taste'},
                    {'name': 'Tahini', 'quantity': '1/4 cup'},
                    {'name': 'Lemon juice', 'quantity': '2 tablespoons'},
                    {'name': 'Maple syrup', 'quantity': '1 teaspoon'},
                    {'name': 'Water', 'quantity': '2-3 tablespoons'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Preheat oven to 400°F (200°C).'},
                    {'number': 2, 'description': 'Cook quinoa according to package instructions.'},
                    {'number': 3, 'description': 'Toss sweet potatoes and chickpeas with 1 tablespoon olive oil, cumin, paprika, salt, and pepper.'},
                    {'number': 4, 'description': 'Spread on a baking sheet and roast for 20-25 minutes until tender.'},
                    {'number': 5, 'description': 'Toss broccoli with remaining olive oil and roast for the last 10 minutes.'},
                    {'number': 6, 'description': 'Make the dressing: whisk together tahini, lemon juice, maple syrup, and enough water to reach desired consistency.'},
                    {'number': 7, 'description': 'Assemble bowls with quinoa, roasted vegetables, chickpeas, and fresh vegetables.'},
                    {'number': 8, 'description': 'Drizzle with tahini dressing and serve.'},
                ]
            },
            {
                'title': 'Homemade Pizza',
                'description': 'Classic pizza with homemade dough and fresh toppings',
                'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591',
                'rating': 4.8,
                'total_time': 60,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': '3 cups'},
                    {'name': 'Active dry yeast', 'quantity': '2 1/4 teaspoons (1 packet)'},
                    {'name': 'Sugar', 'quantity': '1 teaspoon'},
                    {'name': 'Salt', 'quantity': '1 teaspoon'},
                    {'name': 'Warm water', 'quantity': '1 cup'},
                    {'name': 'Olive oil', 'quantity': '2 tablespoons'},
                    {'name': 'Tomato sauce', 'quantity': '1 cup'},
                    {'name': 'Mozzarella cheese', 'quantity': '2 cups, shredded'},
                    {'name': 'Fresh basil', 'quantity': '1/4 cup, chopped'},
                    {'name': 'Oregano', 'quantity': '1 teaspoon, dried'},
                    {'name': 'Garlic', 'quantity': '2 cloves, minced'},
                    {'name': 'Pepperoni slices', 'quantity': '1/2 cup (optional)'},
                    {'name': 'Bell peppers', 'quantity': '1, sliced (optional)'},
                    {'name': 'Mushrooms', 'quantity': '1 cup, sliced (optional)'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large bowl, dissolve yeast and sugar in warm water. Let stand for 10 minutes until frothy.'},
                    {'number': 2, 'description': 'Add salt, olive oil, and 2 1/2 cups of flour. Mix until smooth.'},
                    {'number': 3, 'description': 'Gradually add remaining flour to form a soft dough.'},
                    {'number': 4, 'description': 'Knead on a floured surface for 6-8 minutes until elastic.'},
                    {'number': 5, 'description': 'Place in a greased bowl, cover, and let rise for 30 minutes in a warm place.'},
                    {'number': 6, 'description': 'Preheat oven to 450°F (230°C).'},
                    {'number': 7, 'description': 'Punch down dough and roll out on a floured surface to desired thickness.'},
                    {'number': 8, 'description': 'Transfer to a pizza pan or baking sheet.'},
                    {'number': 9, 'description': 'Spread tomato sauce over crust, sprinkle with garlic and oregano.'},
                    {'number': 10, 'description': 'Add cheese and desired toppings.'},
                    {'number': 11, 'description': 'Bake for 15-20 minutes until crust is golden and cheese is bubbly.'},
                    {'number': 12, 'description': 'Sprinkle with fresh basil before serving.'},
                ]
            },
            {
                'title': 'Beef Rendang',
                'description': 'Indonesian beef stew with rich coconut and spice flavors',
                'image_url': 'https://images.unsplash.com/photo-1651523111529-c1ef15f8a2f3',
                'rating': 4.9,
                'total_time': 180,
                'status': 'published',
                'category': 'Dinner',
                'ingredients': [
                    {'name': 'Beef chuck', 'quantity': '1 kg, cubed'},
                    {'name': 'Coconut milk', 'quantity': '2 cups'},
                    {'name': 'Lemongrass', 'quantity': '2 stalks, bruised'},
                    {'name': 'Kaffir lime leaves', 'quantity': '4'},
                    {'name': 'Galangal', 'quantity': '3 cm piece, sliced'},
                    {'name': 'Turmeric', 'quantity': '1 teaspoon, ground'},
                    {'name': 'Ginger', 'quantity': '3 cm piece, sliced'},
                    {'name': 'Garlic', 'quantity': '5 cloves'},
                    {'name': 'Shallots', 'quantity': '8, peeled'},
                    {'name': 'Red chilies', 'quantity': '10, seeded'},
                    {'name': 'Vegetable oil', 'quantity': '3 tablespoons'},
                    {'name': 'Salt', 'quantity': '1 teaspoon'},
                    {'name': 'Palm sugar', 'quantity': '2 tablespoons'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'Blend shallots, garlic, ginger, galangal, turmeric, and chilies into a smooth paste.'},
                    {'number': 2, 'description': 'Heat oil in a large pot over medium heat. Add the spice paste and cook until fragrant, about 5 minutes.'},
                    {'number': 3, 'description': 'Add lemongrass, kaffir lime leaves, and beef. Stir to coat with the spice paste.'},
                    {'number': 4, 'description': 'Pour in coconut milk, bring to a boil, then reduce heat to low.'},
                    {'number': 5, 'description': 'Add salt and palm sugar, stir well.'},
                    {'number': 6, 'description': 'Simmer uncovered, stirring occasionally, for about 2-3 hours until the meat is tender and the sauce has thickened.'},
                    {'number': 7, 'description': 'The oil will eventually separate from the coconut milk and the meat will turn dark brown.'},
                    {'number': 8, 'description': 'Serve with steamed rice.'},
                ]
            },
            {
                'title': 'Lemon Blueberry Pancakes',
                'description': 'Fluffy pancakes with fresh blueberries and lemon zest',
                'image_url': 'https://images.unsplash.com/photo-1528207776546-365bb710ee93',
                'rating': 4.7,
                'total_time': 30,
                'status': 'published',
                'category': 'Breakfast',
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': '2 cups'},
                    {'name': 'Baking powder', 'quantity': '2 teaspoons'},
                    {'name': 'Baking soda', 'quantity': '1/2 teaspoon'},
                    {'name': 'Salt', 'quantity': '1/4 teaspoon'},
                    {'name': 'Sugar', 'quantity': '3 tablespoons'},
                    {'name': 'Eggs', 'quantity': '2, beaten'},
                    {'name': 'Buttermilk', 'quantity': '2 cups'},
                    {'name': 'Unsalted butter', 'quantity': '3 tablespoons, melted'},
                    {'name': 'Vanilla extract', 'quantity': '1 teaspoon'},
                    {'name': 'Lemon zest', 'quantity': '1 tablespoon'},
                    {'name': 'Fresh blueberries', 'quantity': '1 1/2 cups'},
                    {'name': 'Maple syrup', 'quantity': 'For serving'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large bowl, whisk together flour, baking powder, baking soda, salt, and sugar.'},
                    {'number': 2, 'description': 'In another bowl, combine eggs, buttermilk, melted butter, vanilla extract, and lemon zest.'},
                    {'number': 3, 'description': 'Pour the wet ingredients into the dry ingredients and stir just until combined. Do not overmix.'},
                    {'number': 4, 'description': 'Gently fold in the blueberries.'},
                    {'number': 5, 'description': 'Heat a griddle or large non-stick pan over medium heat and lightly grease with butter.'},
                    {'number': 6, 'description': 'Pour 1/4 cup of batter onto the griddle for each pancake.'},
                    {'number': 7, 'description': 'Cook until bubbles form on the surface, about 2-3 minutes, then flip and cook until golden brown.'},
                    {'number': 8, 'description': 'Serve warm with maple syrup.'},
                ]
            },
            {
                'title': 'Miso Ramen',
                'description': 'Japanese noodle soup with savory miso broth and toppings',
                'image_url': 'https://images.unsplash.com/photo-1557872943-16a5ac26437e',
                'rating': 4.8,
                'total_time': 45,
                'status': 'published',
                'category': 'Soup',
                'ingredients': [
                    {'name': 'Ramen noodles', 'quantity': '4 portions'},
                    {'name': 'Pork belly', 'quantity': '400g, sliced'},
                    {'name': 'Miso paste', 'quantity': '4 tablespoons'},
                    {'name': 'Chicken stock', 'quantity': '6 cups'},
                    {'name': 'Garlic', 'quantity': '4 cloves, minced'},
                    {'name': 'Ginger', 'quantity': '2 tablespoons, grated'},
                    {'name': 'Green onions', 'quantity': '4, chopped'},
                    {'name': 'Soft-boiled eggs', 'quantity': '4'},
                    {'name': 'Corn kernels', 'quantity': '1 cup, cooked'},
                    {'name': 'Bean sprouts', 'quantity': '2 cups'},
                    {'name': 'Nori sheets', 'quantity': '4, cut into strips'},
                    {'name': 'Sesame oil', 'quantity': '1 tablespoon'},
                    {'name': 'Sake', 'quantity': '2 tablespoons'},
                    {'name': 'Soy sauce', 'quantity': '2 tablespoons'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large pot, bring chicken stock to a simmer.'},
                    {'number': 2, 'description': 'Add garlic, ginger, sake, and soy sauce. Simmer for 10 minutes.'},
                    {'number': 3, 'description': 'In a small bowl, mix miso paste with a ladleful of hot broth until dissolved.'},
                    {'number': 4, 'description': 'Pour the miso mixture back into the pot and whisk to combine. Keep warm.'},
                    {'number': 5, 'description': 'In a separate pan, cook pork belly slices until browned and crispy on the edges.'},
                    {'number': 6, 'description': 'Cook ramen noodles according to package instructions, then drain.'},
                    {'number': 7, 'description': 'Divide noodles among four bowls. Ladle the miso broth over the noodles.'},
                    {'number': 8, 'description': 'Top with pork belly, soft-boiled egg halves, corn, bean sprouts, and green onions.'},
                    {'number': 9, 'description': 'Add nori strips on the side and drizzle with sesame oil before serving.'},
                ]
            },
            {
                'title': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream',
                'image_url': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9',
                'rating': 4.9,
                'total_time': 240,
                'status': 'published',
                'category': 'Dessert',
                'ingredients': [
                    {'name': 'Egg yolks', 'quantity': '6'},
                    {'name': 'Sugar', 'quantity': '3/4 cup'},
                    {'name': 'Mascarpone cheese', 'quantity': '500g'},
                    {'name': 'Heavy cream', 'quantity': '1 cup'},
                    {'name': 'Ladyfinger cookies', 'quantity': '24'},
                    {'name': 'Strong coffee', 'quantity': '1 1/2 cups, cooled'},
                    {'name': 'Coffee liqueur', 'quantity': '2 tablespoons'},
                    {'name': 'Unsweetened cocoa powder', 'quantity': '2 tablespoons'},
                    {'name': 'Dark chocolate', 'quantity': '50g, grated'},
                    {'name': 'Vanilla extract', 'quantity': '1 teaspoon'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a heatproof bowl, whisk together egg yolks and sugar. Place over a pot of simmering water.'},
                    {'number': 2, 'description': 'Cook, whisking constantly, until the mixture reaches 160°F (70°C) or thickens enough to coat the back of a spoon.'},
                    {'number': 3, 'description': 'Remove from heat and let cool slightly. Then whisk in the mascarpone cheese until smooth.'},
                    {'number': 4, 'description': 'In a separate bowl, whip the heavy cream and vanilla extract until stiff peaks form.'},
                    {'number': 5, 'description': 'Fold the whipped cream gently into the mascarpone mixture.'},
                    {'number': 6, 'description': 'Mix coffee and coffee liqueur in a shallow dish.'},
                    {'number': 7, 'description': 'Quickly dip each ladyfinger into the coffee mixture (don\'t soak them) and arrange in a single layer in a 9x13 inch dish.'},
                    {'number': 8, 'description': 'Spread half of the mascarpone mixture over the ladyfingers.'},
                    {'number': 9, 'description': 'Repeat with another layer of dipped ladyfingers and the remaining mascarpone mixture.'},
                    {'number': 10, 'description': 'Dust the top with cocoa powder and sprinkle with grated chocolate.'},
                    {'number': 11, 'description': 'Cover and refrigerate for at least 4 hours, preferably overnight.'},
                ]
            },
            {
                'title': 'Greek Salad',
                'description': 'Fresh Mediterranean salad with chunks of vegetables, feta cheese, and olives',
                'image_url': 'https://images.unsplash.com/photo-1551248429-40975aa4de74',
                'rating': 4.6,
                'total_time': 15,
                'status': 'published',
                'category': 'Salad',
                'ingredients': [
                    {'name': 'Cucumber', 'quantity': '1 large, chopped'},
                    {'name': 'Tomatoes', 'quantity': '4 medium, chopped'},
                    {'name': 'Red onion', 'quantity': '1/2, thinly sliced'},
                    {'name': 'Green bell pepper', 'quantity': '1, chopped'},
                    {'name': 'Kalamata olives', 'quantity': '1/2 cup, pitted'},
                    {'name': 'Feta cheese', 'quantity': '200g, cubed'},
                    {'name': 'Extra virgin olive oil', 'quantity': '1/4 cup'},
                    {'name': 'Red wine vinegar', 'quantity': '2 tablespoons'},
                    {'name': 'Dried oregano', 'quantity': '1 teaspoon'},
                    {'name': 'Salt', 'quantity': 'To taste'},
                    {'name': 'Black pepper', 'quantity': 'To taste'},
                ],
                'instructions': [
                    {'number': 1, 'description': 'In a large bowl, combine chopped cucumber, tomatoes, bell pepper, and red onion.'},
                    {'number': 2, 'description': 'Add olives and feta cheese.'},
                    {'number': 3, 'description': 'In a small bowl, whisk together olive oil, red wine vinegar, oregano, salt, and pepper.'},
                    {'number': 4, 'description': 'Pour dressing over the salad and toss gently to combine.'},
                    {'number': 5, 'description': 'Let sit for 5-10 minutes before serving to allow flavors to meld.'},
                ]
            },
        ]
        
        for data in recipe_data:
            # Find category
            category = next((c for c in categories if c.name == data['category']), None)
            
            # Create recipe
            recipe, created = Recipe.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'image_url': data['image_url'],
                    'rating': data['rating'],
                    'total_time': data['total_time'],
                    'status': data['status'],
                    'created_by': user,
                    'category': category,
                }
            )
            
            if created:
                self.stdout.write(f'Created recipe: {recipe.title}')
                
                # Create ingredients
                for ing_data in data['ingredients']:
                    Ingredient.objects.create(
                        name=ing_data['name'],
                        quantity=ing_data['quantity'],
                        recipe=recipe
                    )
                
                # Create instructions
                for inst_data in data['instructions']:
                    Instruction.objects.create(
                        number=inst_data['number'],
                        description=inst_data['description'],
                        recipe=recipe
                    ) 