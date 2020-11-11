from django.urls import path
from .views import *

urlpatterns = [
	path('', main_page, name='main_page_url'),
	path('news/', all_news_page, name='all_news_url'),
	path('news/<str:slug>/', NewsDetail.as_view(), name='news_page_url'),
	path('price/', price_page, name='price_page_url'),
	path('shop/', shop_page, name='shop_page_url'),
	path('shop/item/', item_page, name='item_page_url'),
]