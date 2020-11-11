from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import *

def main_page(request):
	return render(request, 'barber_app/index.html')
	
def all_news_page(request):
	return render(request, 'barber_app/news.html')
	
def price_page(request):
	return render(request, 'barber_app/price.html')

def shop_page(request):
	return render(request, 'barber_app/shop.html')

def item_page(request):
	return render(request, 'barber_app/item.html')

class NewsDetail():
	def get(self, request, slug):
		news = get_object_or_404(News, slug__iexact=slug)
		return render(request, 'barber_app/news_detail.html', {'news': news})