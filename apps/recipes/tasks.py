from .methods import review_recipe
from huey.contrib.djhuey import task

@task()
def task_review_recipe(recipe_id):
  review_recipe(recipe_id)
