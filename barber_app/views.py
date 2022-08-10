from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import *
from .cart import Cart
from .forms import CartAddGoodForm, OrderCreateForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, RecordForm

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

def main_page(request):	
	recordform = RecordForm()
	pasts_news = News.objects.all()[:2]
	content = {'pasts_news': pasts_news, 'recordform': recordform}	
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
	services = Price.objects.all()
	return render(request, 'barber_app/price.html', {'services': services})


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
		cart_good_form = CartAddGoodForm()
		return render(request, 'barber_app/item.html', {'item': item, 'cart_good_form': cart_good_form})		
		


@require_POST
def cart_add(request, good_id):
	cart = Cart(request)
	good = get_object_or_404(Goods, id=good_id)
	form = CartAddGoodForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(good=good, quantity=cd['quantity'], update_quantity=cd['update'])
	return redirect('cart_detail')

def cart_remove(request, good_id):
	cart = Cart(request)
	good = get_object_or_404(Goods, id=good_id)
	cart.remove(good)
	return redirect('cart_detail')

def cart_detail(request):
	cart = Cart(request)	
	for item in cart:
		item['update_quantity_form'] = CartAddGoodForm(initial={'quantity': item['quantity'], 'update': True})
	return render(request, 'barber_app/cart_detail.html', {'cart': cart})


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		order_create_form = OrderCreateForm(request.POST)
		if order_create_form.is_valid():
			order = order_create_form.save()
			for item in cart:
				OrderItem.objects.create(order=order, good=item['good'], price=item['price'], quantity=item['quantity'])
							 
			# Очищаем корзину.
			cart.clear()
			order_created(order.id)
			if request.user.is_authenticated:
				user = User.objects.get(id=request.user.id)  
				profile = Profile.objects.filter(user=user).get()				
				order.profile = profile
				order.save()				
			return render(request, 'barber_app/order_created.html', {'order': order})
	else:
		order_create_form = OrderCreateForm()
	return render(request, 'barber_app/order_create.html', {'cart': cart, 'order_create_form': order_create_form})

	
def order_created(order_id):
	"""Задача отправки email-уведомлений при успешном оформлении заказа."""
	order = Order.objects.get(id=order_id)
	subject = 'Order nr. {}'.format(order.id)
	message = 'Товарищ {},\n\nВы успешно создали заказ.\Ваш заказ -№{}.'.format(order.first_name, order.id)
	mail_sent = send_mail(subject, message, 'barbershop.django@mail.ru', 	[order.email])
	return mail_sent



@login_required
def dashboard(request):
	return render(request,'barber_app/dashboard.html', {'section': 'dashboard'})
	
	
def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			# Создаем нового пользователя, но пока не сохраняем в базу данных.
			new_user = user_form.save(commit=False)
			# Задаем пользователю зашифрованный пароль.
			new_user.set_password(user_form.cleaned_data['password'])
			# Сохраняем пользователя в базе данных.
			Profile.objects.create(user=new_user)
			new_user.save()
			return render(request, 'barber_app/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request,'barber_app/register.html',{'user_form': user_form})
	
	
@login_required
def profile_edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Профиль успешно обновлен')
		else:
			messages.error(request, 'Ошибка обновления профиля')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request,'barber_app/profile_edit.html', {'user_form': user_form,'profile_form': profile_form})
	
	
@login_required
def show_my_orders(request):
	user = User.objects.get(id=request.user.id)  
	profile = Profile.objects.filter(user=user).get()
	my_orders = profile.profile_orders.all()			
	return render(request, 'barber_app/my_orders.html', {'my_orders': my_orders})
	

def record_create(request):	
	if request.method == 'POST':
		recordform = RecordForm(request.POST)		
		if recordform.is_valid():
			cd = recordform.cleaned_data
			record = Record(name=cd['name'], phone=cd['phone'], date=cd['date'], time=cd['time'])
			record.save()
			return render(request, 'barber_app/record_created.html', {'record': record})
	else:
		return redirect(main_page)