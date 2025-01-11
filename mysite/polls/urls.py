
from django.urls import path
from . import views
from .views import register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'), 
    path('new/', views.post_new, name='post_new'),  
    path('<int:post_id>/', views.post_detail, name='post_detail'),  
    path('register/', register, name='register'),  
    path('login/', views.user_login, name='login'),
    path('login/', auth_views.LogoutView.as_view(), name='logout'),  
    path('<int:post_id>/<str:action>/', views.post_reaction, name='post_reaction') 
    
]
