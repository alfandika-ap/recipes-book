from django.urls import path
from .views import LoginView, RegisterView, DashboardView, LogoutView, SavedRecipesView, RecipesListView, RecipeDetailView, MyRecipesView, AddRecipeView, EditRecipeView, DeleteRecipeView

urlpatterns = [
    path("", LoginView.as_view(), name="login-page"),
    path("register/", RegisterView.as_view(), name="register-page"),
    path("dashboard/", DashboardView.as_view(), name="dashboard-page"),
    path("saved-recipes/", SavedRecipesView.as_view(), name="saved-recipes-page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recipes/", RecipesListView.as_view(), name="recipes-list-page"),
    path("recipe/<str:recipe_id>/", RecipeDetailView.as_view(), name="recipe-detail-page"),
    path("my-recipes/", MyRecipesView.as_view(), name="my-recipes-page"),
    path("add-recipe/", AddRecipeView.as_view(), name="add-recipe-page"),
    path("edit-recipe/<str:recipe_id>/", EditRecipeView.as_view(), name="edit-recipe-page"),
    path("delete-recipe/<str:recipe_id>/", DeleteRecipeView.as_view(), name="delete-recipe"),
]
