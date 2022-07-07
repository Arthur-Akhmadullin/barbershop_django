from django.urls import path
from .views import *

urlpatterns = [
	path('', main_page, name='main_page_url'),
	path('news/', all_news_page, name='all_news_url'),
	path('news/<str:slug>/', NewsDetail.as_view(), name='news_page_url'),
	path('price/', price_page, name='price_page_url'),	
	path('shop/', Shop.as_view(), name='shop_page_url'),
	path('shop/filter/', Shop.as_view(), name='filter'),
	path('shop/<str:good_group_slug>/', Shop.as_view(), name='shop_page_url_by_groups'),	
	path('shop/<str:good_group_slug>/<str:slug>/', ItemDetail.as_view(), name='item_page_url'),	
]