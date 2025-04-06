from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.mixins import LoginCheckMixin
from apps.recipes.models import Recipe, Category, Ingredient, Instruction, RecipeSaved
from django.core.paginator import Paginator
from apps.recipes.tasks import task_review_recipe


class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        authenticate_user = authenticate(request, username=username, password=password)

        if authenticate_user is None:
            messages.error(request, "Invalid Credentials")
            return render(request, "auth/login.html")

        login(request, authenticate_user)
        return redirect("dashboard-page")


class RegisterView(View):
    def get(self, request):
        return render(request, "auth/register.html")

    def post(self, request):

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )

        messages.success(request, "Register berhasil!")

        return redirect("login-page")


class DashboardView(LoginCheckMixin, View):

    def get(self, request):
        return render(request, "recipes-dashboard/page.html")

class RecipesListView(LoginCheckMixin, View):

    def get(self, request):
        search_query = request.GET.get('search', '')
        
        if search_query:
            recipes_list = Recipe.objects.filter(title__icontains=search_query)
        else:
            recipes_list = Recipe.objects.all()
        
        paginator = Paginator(recipes_list, 10)  
        page = request.GET.get('page')
        recipes = paginator.get_page(page)

        context = { 
            'recipes': recipes,
            'search_query': search_query
        }

        return render(request, "recipes-dashboard/page-recipes-list.html", context)


class SavedRecipesView(LoginCheckMixin, View):
    
    def get(self, request):
        saved_recipes = RecipeSaved.objects.filter(user=request.user)
        
        context = {
            'saved_recipes': saved_recipes
        }
        
        return render(request, "recipes-dashboard/page-recipes-save.html", context)

    def post(self, request):
        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)

        if RecipeSaved.objects.filter(recipe=recipe, user=request.user).exists():
            RecipeSaved.objects.filter(recipe=recipe, user=request.user).delete()
        else:
            RecipeSaved.objects.create(recipe=recipe, user=request.user)

        return redirect('saved-recipes-page')

class RecipeDetailView(LoginCheckMixin, View):
    
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        saved_recipe = RecipeSaved.objects.filter(recipe=recipe, user=request.user).exists()
        context = {
            'recipe': recipe,
            'saved_recipe': saved_recipe
        }
        return render(request, "recipes-dashboard/page-recipes-detail.html", context)


class MyRecipesView(LoginCheckMixin, View):
    
    def get(self, request):
        my_recipes = Recipe.objects.filter(created_by=request.user)
        
        context = {
            'my_recipes': my_recipes
        }
        
        return render(request, "recipes-dashboard/page-my-recipes.html", context)


class AddRecipeView(LoginCheckMixin, View):
    
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        
        return render(request, "recipes-dashboard/page-add-recipe.html", context)
    
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        image_url = request.POST.get('image_url', '')
        total_time = request.POST.get('total_time')
        category_id = request.POST.get('category', None)
        status = "review"
        status_notes = request.POST.get('status_notes', '')
        
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            image_url=image_url,
            total_time=total_time,
            created_by=request.user,
            category=category,
            status=status,
            status_notes=status_notes
        )
        
        ingredient_names = request.POST.getlist('ingredient_name[]')
        ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
        
        for i in range(len(ingredient_names)):
            if ingredient_names[i].strip():  
                Ingredient.objects.create(
                    name=ingredient_names[i],
                    quantity=ingredient_quantities[i] if i < len(ingredient_quantities) else '',
                    recipe=recipe
                )
        
        instructions = request.POST.getlist('instruction[]')
        
        for i, instruction_text in enumerate(instructions):
            if instruction_text.strip(): 
                Instruction.objects.create(
                    number=i+1,
                    description=instruction_text,
                    recipe=recipe
                )
        
        # Task runner 
        task_review_recipe(recipe.id)
        
        messages.success(request, "Recipe successfully created")
        return redirect('my-recipes-page')

class EditRecipeView(LoginCheckMixin, View):
    
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id, created_by=request.user)
            categories = Category.objects.all()
            
            context = {
                'recipe': recipe,
                'categories': categories
            }
            
            return render(request, "recipes-dashboard/page-edit-recipe.html", context)
        except Recipe.DoesNotExist:
            return redirect('my-recipes-page')
    
    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id, created_by=request.user)
            
            if recipe.status != "review":
                return redirect('edit-recipe-page', recipe_id=recipe_id)
            
            recipe.title = request.POST.get('title')
            recipe.description = request.POST.get('description', '')
            recipe.image_url = request.POST.get('image_url', '')
            recipe.total_time = request.POST.get('total_time')
            
            category_id = request.POST.get('category', None)
            if category_id:
                try:
                    recipe.category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    recipe.category = None
            else:
                recipe.category = None
            
            recipe.save()
            
            Ingredient.objects.filter(recipe=recipe).delete()
            
            ingredient_names = request.POST.getlist('ingredient_name[]')
            ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
            
            for i in range(len(ingredient_names)):
                if ingredient_names[i].strip():  
                    Ingredient.objects.create(
                        name=ingredient_names[i],
                        quantity=ingredient_quantities[i] if i < len(ingredient_quantities) else '',
                        recipe=recipe
                    )
            
            Instruction.objects.filter(recipe=recipe).delete()
            
            instructions = request.POST.getlist('instruction[]')
            
            for i, instruction_text in enumerate(instructions):
                if instruction_text.strip():  
                    Instruction.objects.create(
                        number=i+1,
                        description=instruction_text,
                        recipe=recipe
                    )
            
            messages.success(request, "Recipe successfully updated")
            return redirect('edit-recipe-page', recipe_id=recipe_id)
            
        except Recipe.DoesNotExist:
            return redirect('my-recipes-page')


class DeleteRecipeView(LoginCheckMixin, View):

    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id, created_by=request.user)
            
            recipe.delete()
            
            messages.success(request, "Recipe successfully deleted")
            return redirect('my-recipes-page')
            
        except Recipe.DoesNotExist:
            return redirect('my-recipes-page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login-page")
