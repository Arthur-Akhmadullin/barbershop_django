from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from .models import *

def main_page(request):
	return render(request, 'barber_app/index.html')
	
def all_news_page(request):
	all_news = News.objects.all()
	return render(request, 'barber_app/news.html', {'all_news': all_news})
	
def price_page(request):
	return render(request, 'barber_app/price.html')

def shop_page(request):
	return render(request, 'barber_app/shop.html')

def item_page(request):
	return render(request, 'barber_app/item.html')

class NewsDetail(View):
	def get(self, request, slug):
		news = get_object_or_404(News, slug__iexact=slug)
		return render(request, 'barber_app/news_detail.html', {'news': news})