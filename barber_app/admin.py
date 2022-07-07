from django.contrib import admin
from .models import *

admin.site.register(News)
admin.site.register(Categories)
admin.site.register(Goods)
admin.site.register(Images)
admin.site.register(GoodGroups)


#from django import forms
#from ckeditor_uploader.widgets import CKEditorUploadingWidget

#class NewsAdminForm(forms.ModelForm):
    #body = forms.CharField(widget=CKEditorUploadingWidget())
    #class Meta:
        #model = News

#class NewsAdmin(admin.ModelAdmin):
    #form = NewsAdminForm

#admin.site.register(News, NewsAdmin)