from django.shortcuts import render, redirect
from .models import Category, Article, Comment, Mark
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
# Create your views here.

def index(request):
    articles = Article.objects.all()
    context = {
        'title': 'Главная страница',
        'articles': articles
    }
    return render(request, 'blog/index.html', context)


class ArticleListView(ListView):  # article_list.html
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'  # Иначе вернется objects
    extra_context = {
        'title': 'Главная страница - PROWEB-БЛОГ'
    }  # Дополнительные статические данные


def category_view(request, pk):
    categories = Category.objects.all()
    category = Category.objects.get(pk=pk)
    articles = Article.objects.filter(category=category)
    context = {
        'categories': categories,
        'title': f'Категория: {category.title}',
        'articles': articles
    }
    return render(request, 'blog/index.html', context)

class CategoryListView(ArticleListView):
    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['pk'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'title': f'Статья: {article.title}',
        'article': article
    }
    return render(request, 'blog/article_detail.html', context)


class ArticleDetailView(DetailView):  # article_detail.html
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Статья: {article.title}'
        context['comments'] = Comment.objects.filter(article=article)
        if self.request.user.is_authenticated:
            mark, created = Mark.objects.get_or_create(article=article,
                                                       user=self.request.user)
            if created:
                context['like'] = False
                context['dislike'] = False
            else:
                context['like'] = mark.like
                context['dislike'] = mark.dislike
        else:
            context['like'] = False
            context['dislike'] = False

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        return context



def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('article', article.pk)
    else:
        form = ArticleForm()
    context = {
        'title': 'Добавить статью',
        'form': form
    }
    return render(request, 'blog/article_form.html', context)


class AddArticleView(CreateView):
    # GET POST делать не надо, класс за вас все сделает
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Добавить статью'
    }


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли в аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Не верный логин/пароль')
                return redirect('login')
        else:
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    return render(request, 'blog/user_login.html', context)



def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # group = Group.objects.get()
            # user.groups(group)
            # login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Войдите в аккаунт')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')

    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'blog/register.html', context)



def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    articles = Article.objects.filter(author=user)
    data = []
    for article in articles:
        likes = len(Mark.objects.filter(article=article, like=True))
        comments = len(Comment.objects.filter(article=article))
        data.append({
            'article': article,
            'likes': likes,
            'comments': comments
        })

    context = {
        'title': 'Страница пользователя',
        'user': user,
        'articles': data
    }
    return render(request, 'blog/profile.html', context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        return redirect('article', pk)


def add_or_delete_mark(request, article_id, action):
    # addlike   adddislike   deletelike   deletedislike
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Mark.objects.get_or_create(user=user, article=article)
        if action == 'addlike':
            mark.like = True
            mark.dislike = False
        if action == 'adddislike':
            mark.like = False
            mark.dislike = True
        if action == 'deletelike':
            mark.like = False
        if action == 'deletedislike':
            mark.dislike = False
        mark.save()
        return redirect('article', article_id)
    else:
        return redirect('login')



class SearchResults(ArticleListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word)
        return articles









