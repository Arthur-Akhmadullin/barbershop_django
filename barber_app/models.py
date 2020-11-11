from django.db import models

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length=250, db_index=True)
	slug = models.SlugField(max_length=250, unique=True)
	body = models.TextField(blank=True)
	date = models.DateField(auto_now_add=True)