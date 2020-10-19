from django.shortcuts import render, redirect
from django.urls import reverse

def main_page(request):
	return render(request, 'barber_app/index.html')
	
def price_page(request):
	return render(request, 'barber_app/price.html')

def shop_page(request):
	return render(request, 'barber_app/shop.html')

def item_page(request):
	return render(request, 'barber_app/item.html')
