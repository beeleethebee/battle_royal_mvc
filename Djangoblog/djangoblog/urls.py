from django.urls import path
from .views import ArticleListView, ArticleCreateView, ArticleDeleteView, ArticleUpdateView, ArticleDetailView, CommentDeleteView

urlpatterns = [
    path('articles_list/', ArticleListView.as_view(), name="articles_list"),
    path('edit/', ArticleCreateView.as_view(), name='article_edit'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name="article_update"),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name="article_delete"),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:article_pk>/delete-comment/<int:pk>', CommentDeleteView.as_view(), name="comment_delete"),
]