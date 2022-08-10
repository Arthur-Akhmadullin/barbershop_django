from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
#from django.utils.text import slugify
from pytils.translit import slugify
from time import time

from datetime import date
from django.conf import settings

# Create your models here.
class News(models.Model):
	title = models.CharField(max_length=250, db_index=True)
	slug = models.SlugField(max_length=250, unique=True)
	#body = models.TextField(blank=True)
	body = RichTextUploadingField(blank=True, null=True)
	date = models.DateField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('news_page_url', kwargs={'slug': self.slug})
		
	class Meta:
		ordering = ['-date']



class Goods(models.Model):
	category = models.ForeignKey('Categories', on_delete=models.PROTECT, default=None, related_name='goods')	
	name = models.CharField(max_length=35, db_index=True)
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	article = models.CharField(max_length=20, db_index=True)
	preview_image = models.ImageField(upload_to='gallery_products', blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=0)
	available = models.BooleanField(default=True)
	short_description = models.TextField(blank=True)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	good_group = models.ForeignKey('GoodGroups', on_delete=models.PROTECT, default=None, related_name='goodgroup')
	
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('item_page_url', kwargs={'good_group_slug': self.good_group.slug, 'slug': self.slug})
		
	#def get_update_url(self):
		#return reverse('post_update_url', kwargs={'slug': self.slug})
		
	#def get_delete_url(self):
		#return reverse('post_delete_url', kwargs={'slug': self.slug})
	
		
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.category) + "-" + gen_slug(self.name) + "-" + str(int(time()))				
		super().save(*args, **kwargs)
		
	class Meta:
		ordering = ['updated']


class Categories(models.Model):	
	category = models.CharField(max_length=30)
	
	def __str__(self):
		return self.category		


class Images(models.Model):
	good = models.ForeignKey('Goods', on_delete=models.CASCADE, default=None, related_name='images')
	image = models.ImageField(upload_to='media/uploads/gallery_products', blank=True)
	
	
class GoodGroups(models.Model):
	good_group = models.CharField(max_length=30)
	slug = models.SlugField(max_length=30, blank=True, unique=True)
	
	def __str__(self):
		return self.good_group


class Order(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=15)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	profile = models.ForeignKey('Profile', related_name='profile_orders', on_delete=models.SET_NULL, null=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

		
class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', 	on_delete=models.CASCADE)
	good = models.ForeignKey(Goods, related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	
	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)
		
		
class Record(models.Model):
	RECORD_TIME = (('10.00','10.00'), ('11.00','11.00'), ('12.00','12.00'), ('13.00','13.00'), ('15.00','15.00'), ('16.00','16.00'), ('17.00','17.00'))
	
	name = models.CharField(max_length=35)
	phone = models.CharField(max_length=15)
	date = models.DateField(auto_now = False)
	time = models.CharField(max_length=5, choices=RECORD_TIME, default=RECORD_TIME[1][1])	
	confirmed = models.BooleanField(default=False)


class Price(models.Model):
	service_name = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=5, decimal_places=0)
	
	
def gen_slug(s):
	return slugify(s)