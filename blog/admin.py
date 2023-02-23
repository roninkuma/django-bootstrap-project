from django.contrib import admin
from .models import Category, Article, Comment
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'views', 'created_at', 'updated_at']
    list_display_links = ['pk', 'title']
    list_filter = ['category', 'created_at']



admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)