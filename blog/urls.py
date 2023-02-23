from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>', category_view, name='category'),
    # path('article/<int:pk>', article_detail, name='article'),
    # path('add_article', add_article, name='add_article')
    path('', ArticleListView.as_view(), name='index'),
    path('category/<int:pk>', CategoryListView.as_view(), name='category'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('add_article', AddArticleView.as_view(), name='add_article'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('profile/<int:user_id>', profile, name='profile'),
    path('save_comment/<int:pk>', save_comment, name='save_comment'),
    path('mark/<int:article_id>/<str:action>', add_or_delete_mark, name='mark'),
    path('search', SearchResults.as_view(), name='search')
]
