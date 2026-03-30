# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'  # ← Namespace для {% url 'blog:...' %}

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/', views.category_list, name='category_list'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('create/', views.post_create, name='post_create'),
    path('category/<slug:slug>/', views.posts_by_category, name='posts_by_category'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]