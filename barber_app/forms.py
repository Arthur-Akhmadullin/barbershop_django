from django import forms
from django.forms import TextInput
from .models import Order, Profile, Record

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddGoodForm(forms.Form):
	# Корзина
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="")
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
	
	#Полю select присваиваем css-класс, чтобы он нормально отображался на странице товара
	quantity.widget.attrs.update({'style': 'display:inline-block;' 'box-sizing: content-box;' 'border-radius:2px;'  'padding-left: 10px;' 'width: 90px;' 'height:42px;' 'font-size: 18px;' 'font-weight:700;' 'text-align:center;'})
	

class OrderCreateForm(forms.ModelForm):
	# Форма для заказа и оформления товаров
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'email', 'address', 'phone']
		widgets = {
			'first_name': TextInput(attrs={'style': 'display:block;' 'width:200px;' 'padding-left: 10px;' 'padding-top:5px;' 'padding-bottom:5px;' 'font-size: 18px;'}),
			'last_name': TextInput(attrs={'style': 'display:block;' 'width:200px;' 'padding-left: 10px;' 'padding-top:5px;' 'padding-bottom:5px;' 'font-size: 18px;'}),
			'email': TextInput(attrs={'style': 'display:block;' 'width:200px;' 'padding-left: 10px;' 'padding-top:5px;' 'padding-bottom:5px;' 'font-size: 18px;'}),
			'address': TextInput(attrs={'style': 'display:block;' 'width:200px;' 'padding-left: 10px;' 'padding-top:5px;' 'padding-bottom:5px;' 'font-size: 18px;'}),
			'phone': TextInput(attrs={'style': 'display:block;' 'width:200px;' 'padding-left: 10px;' 'padding-top:5px;' 'padding-bottom:5px;' 'font-size: 18px;'}),
        }
		labels = {
            'first_name': ('Имя'),
			'last_name': ('Фамилия'),
			'email': ('электронная почта'),
			'address': ('Адрес доставки'),
			'phone': ('Телефон'),
        }
		

#class LoginForm(forms.Form):
	# Авторизация пользователя
	#username = forms.CharField(widget=forms.TextInput(attrs={'class': 'icon-user', 'placeholder': 'Логин'}))
	#password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'icon-password', 'placeholder': 'Пароль'}))
	

class LoginForm(AuthenticationForm):
	username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'icon-user', 'placeholder': 'Логин'}))
	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'icon-password', 'placeholder': 'Пароль'}))
	
	
class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Еще раз пароль', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')
		
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Пароли не совпадают!')
		return cd['password2']
	
	

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

		
class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['date_of_birth']
	

class RecordForm(forms.ModelForm):
	class Meta:
		model = Record
		fields = ['name', 'phone', 'date', 'time', ]
	
		widgets = {
			'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Дата'}),
			'time': forms.Select(attrs={'placeholder': 'Время'}),
			'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
			'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Телефон'}),			
		}
		labels = {
			'date': (''),
			'time': (''),
			'name': (''),
			'phone': (''),	
			}	