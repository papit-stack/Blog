from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('reset-password/<uuid:reset_id>',views.reset_password,name='reset-password'),
    path('post-blog/',views.add_post,name='add_post'),
    path('blog/<slug:slug>/',views.blog_detail, name='blog_detail'),

]
