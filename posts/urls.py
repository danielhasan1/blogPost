from django.conf.urls import url
from django.contrib import admin
from .views import (
	list_details,
	create,
	delete_,
	update_,
	details,
	)

#below is what documentaion says
#but to remove error we pass the callable instead we are using this just to remove the error
#urlpatterns = [
#    
#    url(r'^$',"posts.views.list_details"),
#    url(r'^create/$',"posts.views.create"),
#    url(r'^delete/$',"posts.views.delete_"),
#    url(r'^update/$',"posts.views.update_"),
#    url(r'^details/$',"posts.views.details"),
#]

urlpatterns = [
    
    url(r'^$',list_details,name='list'),
    url(r'^create/$',create),
    url(r'^(?P<id>\d+)/delete/$',delete_),
    url(r'^(?P<id>\d+)/edit/$',update_, name='update'),
    url(r'^(?P<id>\d+)/$',details,name='detail'),
    #url(r'^(?P<id>\d+)/$',comment_delete, name='thread'),
]