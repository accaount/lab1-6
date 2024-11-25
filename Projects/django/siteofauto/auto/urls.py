from django.urls import path, register_converter
from auto import views, converters
from auto.views import serve_auto_icon
from .models import Category
from django.contrib import admin

admin.site.site_header = "Панель администрирования"


urlpatterns = [

    path('', views.index, name='home'),
    path('static/auto/images/logo.ico', serve_auto_icon, name='serve_logo_icon'),
path('', views.index, name='home'),
    path('sedan/<slug:sed_slug>/', views.categories_by_slug, name='sedan'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:sed_slug>/', views.show_category,name='category'),

    path('post/<slug:post_slug>/', views.show_post,name='post'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('admin/', admin.site.urls),
]


register_converter(converters.FourDigitYearConverter, "year4")