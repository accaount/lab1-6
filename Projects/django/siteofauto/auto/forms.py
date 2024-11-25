from django import forms
from .models import Auto
from .admin import AutoAdmin
from .models import Category, Owner
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

@deconstructible
class RussianValidator:
    ALLOWED_CHARS =\
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message,code=self.code, params={"value": value})


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Фото")


class AddPostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок",widget=forms.TextInput(attrs={'class': 'form - input'}),validators = [RussianValidator(),],error_messages = {'min_length': 'Слишком короткий заголовок','required': 'Без заголовка - никак',})

    slug = forms.SlugField(max_length=255, label="URL",validators=[MinLengthValidator(5, message="Минимум 5 символов"), MaxLengthValidator(100, message="Максимум 100символов"),])

    content =forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    sed =forms.ModelChoiceField(queryset=Category.objects.all(),empty_label = "Категория не выбрана", label="Категории")
    owner =forms.ModelChoiceField(queryset=Owner.objects.all(), required=False,label="Хозяин", empty_label="Нет хозяина")



    class Meta:
        model = Auto
        fields = ['title', 'slug', 'content', 'photo',
                  'is_published', 'sed', 'owner', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title
