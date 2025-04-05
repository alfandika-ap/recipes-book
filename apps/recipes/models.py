from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User

STATUS_CHOICES = [
  ("review", "Review"),
  ("published", "Published"),
  ("rejected", "Rejected"),
]

class Category(BaseModel):
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)

class Recipe(BaseModel):
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  image_url = models.TextField(blank=True, null=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.FloatField(default=0)
  total_time = models.IntegerField(default=0)
  status = models.CharField(max_length=255, choices=STATUS_CHOICES)
  status_notes = models.TextField(blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

class Ingredient(BaseModel):
  name = models.CharField(max_length=255)
  quantity = models.CharField(max_length=255)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Instruction(BaseModel):
  number = models.IntegerField()
  description = models.TextField()
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class RecipeSaved(BaseModel):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('recipe', 'user')
