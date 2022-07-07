from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import HttpResponse

from .models import *

def main_page(request):
	pasts_news = News.objects.all()[:2]
	content = {'pasts_news': pasts_news}
	return render(request, 'barber_app/index.html', content)
	
	
def all_news_page(request):
	all_news = News.objects.all()
	
	past_news = all_news.first()	
	
	left_news = all_news[1:all_news.count():2]	
	right_news = all_news[2:all_news.count():2]		
	zip_news = zip(left_news, right_news)
	
	if all_news.count()%2 == 0:
		first_news = all_news.last()	
	
	content = {'past_news': past_news, 'zip_news': zip_news, 'first_news': first_news}
	return render(request, 'barber_app/news.html', content)
	

class NewsDetail(View):
	def get(self, request, slug):
		news = get_object_or_404(News, slug__iexact=slug)
		return render(request, 'barber_app/news_detail.html', {'news': news})
		

def price_page(request):
	return render(request, 'barber_app/price.html')


class Shop(View):
	def get(self, request, good_group_slug=None):	
		#Определяем вид фильтра
		filterCheckPoints = {}
		isFilter = False
		good_group = None
		
		groups_in_form = GoodGroups.objects.all().order_by('good_group')
				
		names_in_form = Goods.objects.all()
		names_set = set()
		for name in names_in_form:
			names_set.add(name.__str__())
		names_set = sorted(names_set)
		
		queryset = Goods.objects.all()
		if good_group_slug:
			good_group = get_object_or_404(GoodGroups, slug__iexact=good_group_slug)
			queryset = queryset.filter(good_group=good_group)
			filterCheckPoints.update(good_group=good_group.id)			
		
		if self.request.GET.get("good_group"):
			queryset = queryset.filter(good_group=self.request.GET.get("good_group"))
			filterCheckPoints.update(good_group=int(self.request.GET.get("good_group")))
			isFilter = True
		
		if self.request.GET.getlist("name"):
			queryset = queryset.filter(name__in=self.request.GET.getlist("name"))
			filterCheckPoints.update(name=self.request.GET.getlist("name"))
			isFilter = True
		
					
		filterRequestPath = self.request.get_full_path()
		filterRequestPath = filterRequestPath[filterRequestPath.find('?'):]
		if "&page" in filterRequestPath:
			filterRequestPath = ('&'.join(filterRequestPath.split('&')[:-1]))
		
			
		paginator = Paginator(queryset, 2)
		page_number = request.GET.get('page', 1) #page - параметр get-запроса в адресной строке, 1 - ззначение по-умолчанию, на тот случай, если нужного значения page не существует (чтобы не возбуждать исключение)
		page_goods = paginator.get_page(page_number)		
		is_paginated = page_goods.has_other_pages()
			
				
		
		context = {'goods': page_goods,
					'is_paginated': is_paginated,
					'groups_in_form': groups_in_form,
					'names_set': names_set,
					'isFilter': isFilter,
					'filterRequestPath': filterRequestPath,
					'filterCheckPoints': filterCheckPoints,
					'good_group': good_group}
				
		return render(request, 'barber_app/shop.html', context)
	
	
class ItemDetail(View):
	def get(self, request, good_group_slug, slug):		
		good_group = get_object_or_404(GoodGroups, slug__iexact=good_group_slug)
		item = get_object_or_404(Goods, good_group=good_group, slug__iexact=slug)
		return render(request, 'barber_app/item.html', {'item': item})
		#item = get_object_or_404(Goods, slug__iexact=slug)
		#return render(request, 'barber_app/item.html', {'item': item})
		
		
#def item_page(request, slug):
	#item = get_object_or_404(Goods, slug__iexact=slug)
	#content = {'item': item}	
	#return render(request, 'barber_app/item.html')
	#item = Goods.objects.get(slug__iexact=slug)
	#return render(request, 'barber_app/item2.html', context={'item': item})
		
		
def shop_page(request, good_group_slug=None):
	if good_group_slug:
		good_group = get_object_or_404(GoodGroups, slug__iexact=good_group_slug)
		goods = Goods.objects.filter(good_group=good_group)
	else:
		good_group = None
		goods = Goods.objects.all()
		
	paginator = Paginator(goods, 3)
	page_number = request.GET.get('page', 1) #page - параметр get-запроса в адресной строке, 1 - ззначение по-умолчанию, на тот случай, если нужного значения page не существует (чтобы не возбуждать исключение)
	page_goods = paginator.get_page(page_number)
	is_paginated = page_goods.has_other_pages()
	
	groups_in_form = GoodGroups.objects.all().order_by('good_group')
	
	names_in_form = Goods.objects.all()
	names_set = set()
	for name in names_in_form:
		names_set.add(name.__str__())
	names_set = sorted(names_set)
		
	
	context = {'goods': page_goods,
				'is_paginated': is_paginated,
				'groups_in_form': groups_in_form,
				'names_set': names_set,
				'good_group': good_group}
				
	return render(request, 'barber_app/shop.html', context)
	
	
class FilterGoods(View):
	def get(self, request):	
		filterCheckPoints = {}	
	
		if self.request.GET.get("good_group"):
			queryset = Goods.objects.filter(good_group = self.request.GET.get("good_group"))
			filterCheckPoints.update(good_group = int(self.request.GET.get("good_group")))
		else:
			queryset = Goods.objects.all()

		if self.request.GET.getlist("name"):
			queryset = queryset.filter(name__in = self.request.GET.getlist("name"))
			filterCheckPoints.update(name = self.request.GET.getlist("name"))
		
		
		#queryset = Goods.objects.filter(Q(name__in = self.request.GET.getlist("name", "")) & Q(good_group = self.request.GET.get("good_group", "")))
			
		stroka = self.request.get_full_path()
		stroka = stroka[stroka.find('?'):]
		if "&page" in stroka:
			stroka = ('&'.join(stroka.split('&')[:-1]))
		
			
		paginator = Paginator(queryset, 2)
		page_number = request.GET.get('page', 1) #page - параметр get-запроса в адресной строке, 1 - ззначение по-умолчанию, на тот случай, если нужного значения page не существует (чтобы не возбуждать исключение)
		page_goods = paginator.get_page(page_number)
		is_paginated = page_goods.has_other_pages()
		
		groups_in_form = GoodGroups.objects.all().order_by('good_group')
				
		names_in_form = Goods.objects.all()
		names_set = set()
		for name in names_in_form:
			names_set.add(name.__str__())
		names_set = sorted(names_set)
			
		isFilter = True	
		
		
		context = {'goods': page_goods,
					'is_paginated': is_paginated,
					'groups_in_form': groups_in_form,
					'names_set': names_set,
					'isFilter': isFilter,
					'stroka': stroka,
					'filterCheckPoints': filterCheckPoints}
				
		return render(request, 'barber_app/shop.html', context)