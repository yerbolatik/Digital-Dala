from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>/', views.post_detail, name='post'),
    path('create-post/', views.create_post, name='create_post'),
    # path('registration/', views.registration_view, name='registration'),
    # path('photo/<int:pk>/', viewis.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/like/', views.like_photo, name='like_photo'),
    path('photo/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/<int:pk>/like/', views.like_news, name='like_news'),
    path('news/<int:pk>/comment/', views.add_comment, name='add_comment'),

]
