from django.contrib import admin
from auto.models import Auto
from django.db import models
from .models import Category
from django.utils.safestring import mark_safe


class MarFilter(admin.SimpleListFilter):
    title = 'Статус авто'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('mar','С хозяином'),
            ('unmar', 'Без хозяина')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'mar':
            return queryset.filter(owner__isnull=False)

        elif self.value() == 'unmar':

            return queryset.filter(owner__isnull=True)

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ['title', 'slug', 'content', 'photo','post_photo', 'sed',
              'owner', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title','post_photo', 'time_create',
                    'is_published', 'sed')

    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 3
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith' , 'sed__name']
    list_filter = [MarFilter, 'sed__name', 'is_published']

    @admin.display(description="Изображение")
    def post_photo(self, auto: Auto):
        if auto.photo:
            return mark_safe(f"<img src = '{auto.photo.url}'width = 50 > ")
        return "Без фото"


    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Auto.Status.PUBLISHED)
        self.message_user(request,f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count =queryset.update(is_published=Auto.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей)сняты с публикации!", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


