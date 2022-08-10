from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
	path('', main_page, name='main_page_url'),
	path('news/', all_news_page, name='all_news_url'),
	path('news/<str:slug>/', NewsDetail.as_view(), name='news_page_url'),
	path('price/', price_page, name='price_page_url'),	
	#path('login/', user_login, name='login'),
	path('account/', dashboard, name='dashboard'),
	path('account/login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
	path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('account/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('account/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('account/register/', register, name='register'),
	path('account/profile_edit/', profile_edit, name='profile_edit'),
	path('account/my_orders/', show_my_orders, name='my_orders'),
	#path('record/', record_create, name='record'),
	path('record_created/', record_create, name='record'),
	path('cart/', cart_detail, name='cart_detail'),
	path('cart/add/<int:good_id>/', cart_add, name='cart_add'),
	path('cart/remove/<int:good_id>/', cart_remove, name='cart_remove'),
	path('orders/create/', order_create, name='order_create'),
	path('shop/', Shop.as_view(), name='shop_page_url'),
	path('shop/filter/', Shop.as_view(), name='filter'),
	path('shop/<str:good_group_slug>/', Shop.as_view(), name='shop_page_url_by_groups'),	
	path('shop/<str:good_group_slug>/<str:slug>/', ItemDetail.as_view(), name='item_page_url'),	
]