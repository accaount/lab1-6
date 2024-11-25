from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator,MaxLengthValidator

def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д':
'd',
 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и':
'i', 'к': 'k',
 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п':
'p', 'р': 'r',
 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х':
'h', 'ц': 'c', 'ч': 'ch',
 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y',
'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
    return "".join(map(lambda x: d[x] if d.get(x,
False) else x, s.lower()))


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Auto(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,verbose_name="Заголовок")
    slug = models.SlugField(max_length=255,db_index=True, unique=True, validators=[MinLengthValidator(5),MaxLengthValidator(100),])

    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x:(bool(x[0]), x[1]), Status.choices)),default=Status.DRAFT, verbose_name="Статус")
    sed = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank =True, related_name='tags', verbose_name="Тэги")
    owner = models.OneToOneField('Owner',on_delete=models.SET_NULL, null=True, blank=True,related_name='cars', verbose_name="Хозяин")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",default=None, blank=True, null=True,verbose_name="Фото")


    objects = models.Manager()  # стандартный менеджер

    class Meta:
        verbose_name = 'Автомобильный журнал'
        verbose_name_plural = 'Автомобильный журнал'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    # Менеджер для опубликованных постов
    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=Auto.Status.PUBLISHED)  # фильтрация по публикации

    # Используем кастомный менеджер
    published = PublishedManager()


class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255,unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'sed_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
        tag = models.CharField(max_length=100, db_index= True)
        slug = models.SlugField(max_length=255, unique=True, db_index=True)

        def get_absolute(self):
            return reverse('tag', kwargs={'tag_slug': self.slug})

        def __str__(self):
            return self.tag

class Owner(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name