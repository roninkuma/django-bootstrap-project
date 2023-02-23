from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')  # VARCHAR(255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Здесь будет описание', verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    # blank=True - не обязательна для заполнения, null=True - можено быть пустой в базе
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # Автоматически возьмет время создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления') # Время последнего изменения
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def get_photo(self):
        if self.photo:
            url = self.photo.url
        else:
            url = 'http://artinblog.ru/uploads/posts/2013-04/1367159240_300x200.jpg'
        return url


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Создать модель Комментария которая знает
# Пользователь, Текст, Статья, Дата создания
# Реализовать форму, в котору пользователь будет писать ТЕКСТ
# Реализавать вьюшку, которая будет сохранять комментарий
# Доработать вьюшку деталей статьи и выводить форму, уже созданные
# комментари к этой статье

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return f'{self.article} - {self.like} / {self.dislike}'

    class Meta:
        verbose_name = 'Лайк и Дизлайк'
        verbose_name_plural = 'Лайки и дизайки'
