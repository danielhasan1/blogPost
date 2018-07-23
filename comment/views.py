
from django.shortcuts import render, get_object_or_404,redirect,Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from.forms import PostForm
#from comment.form import CommentForm
from comment.models import comment as Comment
from django.contrib.contenttypes.models import ContentType
from posts import views
from .form import CommentForm
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required(login_url="/login/")
def deleteth(request,id):
	objc=get_object_or_404(Comment,id=id)
	if not objc.is_parent:
		if request.method=="POST":
			print("child")
	
	#obj=get_object_or_404(Comment,id=id)
	try:
		obj=get_object_or_404(Comment,id=id)
	except:
		raise Http404
	if obj.user != request.user:
		response = HttpResponse("you do not have permission")
		response.status_code = 403
		return response
		#raise Http404
	if request.method=="POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		
		obj.delete()
		return HttpResponseRedirect(parent_obj_url)
	
	context = {
	"obj":obj,

	}
	return render(request,"delete.html",context)

def com_thr(request,id):
	#obj=get_object_or_404(Comment,id=id)
	try:
		obj=get_object_or_404(Comment,id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj = obj.parent 

	content_obj = obj.content_object
	content_id=obj.content_object.id
	initial_data = {
			"content_type":obj.content_type,
			"object_id":obj.object_id,
	}
	form=CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
	    c_type = form.cleaned_data.get("content_type")
	    content_type = ContentType.objects.get(model=c_type)
	    obj_id = form.cleaned_data.get("object_id")
	    content_data = form.cleaned_data.get("content")
	    parent_obj = None
	    try:
	    	parent_id = int(request.POST.get("parent_id"))
	    except:
	    	parent_id=None

	    if parent_id:
	    	parent_qs = Comment.objects.filter(id=parent_id)
	    	if parent_qs.exists() and parent_qs.count()==1:
	    	    parent_obj = parent_qs.first()

	    new_comment, created = Comment.objects.get_or_create(
	    							user = request.user,
	    							content_type = content_type,
	    							object_id = obj_id,
	    							content = content_data,
	    							parent = parent_obj,
	    							)
	    return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
	context={
	"com":obj,
	"form":form,
	"pre":content_obj,
	}
	return render(request,"thread.html",context)
    