"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from acounts.views import (login_view, logout_view, register_view)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$',"posts.views.loginpage"),
    url(r'^bootstrap/$',TemplateView.as_view(template_name='bootstrap/example.html')),
    
    url(r'^comment/',include("comment.urls", namespace='comment')),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/',logout_view,name='logout'),
    url(r'^register/',register_view,name='register'),
    url(r'^',include("posts.urls", namespace='posts')),
   # url(r'^login/$',auth_views.login, name='login'),
    #url(r'^logout/$',auth_views.logout,{'next_page':'/login'}, name='logout'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)