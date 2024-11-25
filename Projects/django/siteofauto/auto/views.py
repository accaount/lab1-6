from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import uuid
from .forms import AddPostForm, UploadFileForm
from .models import Auto
from .models import Category

def index(request):

    data ={
        'title': 'Главная страница',
        'menu': menu,
        'posts': Auto.published.all(),
        'sed_selected': 0,
    }

    return render(request, 'auto/index.html', context=data)


def categories_by_slug(request, sed_slug):
    if request.GET:
        print(request.GET)

    return HttpResponse(f"<h1>Статьи покатегориям</h1><p >slug: {sed_slug}</p>")

def archive(request, year):
    if year > 2023:
        return redirect('home',permanent=True)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name':'add_page'},
    {'title': "Обратная связь", 'url_name':'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
         form = AddPostForm()

    return render(request, 'auto/addpage.html',{'menu': menu, 'title': 'Добавление статьи', 'form':form})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def show_category(request, sed_slug):
    category = get_object_or_404(Category,slug=sed_slug)
    posts = Auto.published.filter(sed_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
 }

    return render(request, 'auto/index.html',
context=data)


def handle_uploaded_file(f):
    name = f.name
    ext = ''

    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
#handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'auto/about.html', {'title':'О сайте', 'menu': menu, 'form': form})


def show_post(request, post_slug):
    post = get_object_or_404(Auto, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'sed_selected': 1,
 }

    return render(request, 'auto/post.html',
context=data)



def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts =tag.tags.filter(is_published=Auto.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
 }
    return render(request, 'auto/index.html',
context=data)
