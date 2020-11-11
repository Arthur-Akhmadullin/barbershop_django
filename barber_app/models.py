from django.db import models
from django.shortcuts import reverse

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length=250, db_index=True)
	slug = models.SlugField(max_length=250, unique=True)
	body = models.TextField(blank=True)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

	#def get_absolute_url(self):
		#return reverse('news_page_url', kwargs={'slug': self.slug})