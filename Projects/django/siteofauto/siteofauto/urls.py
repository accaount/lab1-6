from django.urls import path, register_converter, re_path
from auto import views
from siteofauto import converters
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Панель администрирования"
admin.site.index_title =  "Автомобильный журнал"

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),  # Путь к админ-панели
    path('sedan/<slug:sed_slug>/', views.categories_by_slug, name='sedan'),
    re_path(r'^archive/(?P<year>[0-9]{4})/',views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post,name='post'),
    path('category/<slug:sed_slug>/', views.show_category,name='category'),
    path('post/<slug:post_slug>/', views.show_post,name='post'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

