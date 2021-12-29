"""form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from first.views import index as home
from first.views import register_request as register
from first.views import login_request as login
from first.views import about as about
from first.views import create as create
from first.views import coment as coment
from first.views import HomeView, PostHomeView, AddPostView, UpdatePostView, DeletePostView
from first.views import UserEditView, PasswordsChangeView, ShowProfilePageView,CreateProfilePageView, EditProfilePageView
from first.views import likeView
from django.contrib.auth import views as auth_views
from first.views import password_success as password_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('home/', home),
    path('create/', create, name="create"),
    path('coment/', coment, name="coment"),
    path('register/', register, name="reg"),
    path('login/', login, name="log"),
    path('about/', about, name="homepage"),
    path('about/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name="posts"),
    path('posts/<int:pk>', PostHomeView.as_view(), name="post-detail"),
    path('add_post/', AddPostView.as_view(),name="add_post"),
    path('posts/edit/<int:pk>', UpdatePostView.as_view(),name="update_post"),
    path('posts/<int:pk>/remove', DeletePostView.as_view(),name="delete_post"),
    path('edit_profile/', UserEditView.as_view(),name="edit_profile"),
    path('password/', PasswordsChangeView.as_view(template_name='firstapp/change_password.html')),
    path('password_success/', password_success, name="password_success"),
    path('like/<int:pk>', likeView, name='like_post'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(),name="show_profile_page"),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(),name="edit_profile_page"),       
    path('create_profile_page/', CreateProfilePageView.as_view(),name="create_profile_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)