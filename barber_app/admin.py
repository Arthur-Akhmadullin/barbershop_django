from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(News)
admin.site.register(Categories)
#admin.site.register(Goods)
#admin.site.register(Images)
admin.site.register(GoodGroups)

class ImagesInline(admin.TabularInline):
	fk_name = 'good'
	model = Images

class GoodsAdminForm(forms.ModelForm):
	description = forms.CharField(widget=CKEditorUploadingWidget())
	
	class Meta:
		model = Goods
		fields = '__all__'


	
	
@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price')
	form = GoodsAdminForm
	inlines = [ImagesInline]
	

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['good']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'phone', 'paid', 'created', 'updated']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]
	
	
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth']
	

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
	list_display = ['name', 'phone', 'date', 'time', 'confirmed']
	
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
	list_display = ['service_name', 'price']
	
	
	
	
# Пример вставки поля ckeditor
'''	
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NewsAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

admin.site.register(News, NewsAdmin)
'''