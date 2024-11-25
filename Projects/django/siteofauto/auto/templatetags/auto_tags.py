from django import template
import auto.views as views
from ..models import TagPost
from auto.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('auto/list_categories.html')
def show_categories(sed_selected_id=0):
    seds = Category.objects.all()
    return {"seds": seds, "sed_selected": sed_selected_id}

@register.inclusion_tag('auto/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}