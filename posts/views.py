from django.shortcuts import render, get_object_or_404,redirect,Http404
from django.http import HttpResponse, HttpResponseRedirect
from.forms import PostForm
from comment.form import CommentForm
from comment.models import comment as Comment
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .models import post
from django.db.models import Q

def create(request):
	if not request.user.is_authenticated():
		raise Http404 #in fututre redirect to you must login or signup to post something
	formn = PostForm(request.POST or None, request.FILES or None)
	boole=False
	#if formn.is_valid()
	if formn.is_valid():
	 #print(request.POST.get("title"))
		instance = formn.save(commit=False)
		instance.user = request.user
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : formn,
		"bool":boole
		}
	return render(request,'forms.html',context)

#def loginpage(request):
#	return render(request,"loginview.html")

def details(request,id):
	#instance = post.objects.get(id=1)
	instance = get_object_or_404(post, id=id)

	if instance.draft:
		if not request.user.is_authenticated():
		    raise Http404
	initial_data = {
			"content_type":instance.get_content_type,
			"object_id":instance.id,
	}
	comment_form = CommentForm(request.POST or None, initial=initial_data)
	
	if comment_form.is_valid() and request.user.is_authenticated():
	    c_type = comment_form.cleaned_data.get("content_type")
	    content_type = ContentType.objects.get(model=c_type)
	    obj_id = comment_form.cleaned_data.get("object_id")
	    content_data = comment_form.cleaned_data.get("content")
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
	    return HttpResponseRedirect(instance.get_absolute_url())
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	comments = instance.comments #comment.objects.filter_by_instance(instance)
	context = {
	"instance": instance,
	"title": instance.title,
	"comment":comments,
	"comment_form":comment_form,
	"form_e":form,
	}
	#print(instance.content)
	return render(request,'details.html',context)

def list_details(request):
    query_list=post.objects.active().order_by("-timestamp")
    search_query=request.GET.get('q')
    if search_query:
    	query_list =query_list.filter(
    		Q(title__icontains=search_query) |
    		Q(content__icontains=search_query) |
    		Q(user__first_name__icontains=search_query) |
    		Q(user__last_name__icontains=search_query) |
    		Q(user__username__icontains=search_query)
    		).distinct()
    paginator = Paginator(query_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    

    try:
    	queryset = paginator.page(page)
    except PageNotAnInteger:
    	queryset = paginator.page(1)
    except EmptyPage:
    	queryset = paginator.page(paginator.num_pages)
    #return render(request, 'list.html', context)
    context={
        "obj":queryset,
        "title":"Latest Posts",
    }
    return render(request,'index.html',context)

def delete_(request,id=None):
	if not request.user.is_authenticated():
		raise Http404#in fututre change to redirect to login page if the user is not authenticated or report it.
	try:
		obj=get_object_or_404(post,id=id)
	except:
		raise Http404
	if obj.user != request.user:
		response = HttpResponse("you do not have permission")
		response.status_code = 403
		return response
	#instance = get_object_or_404(post,id=id)
	obj.delete()
	#meesage
	return redirect("posts:list")

def update_(request,id):
	if not request.user.is_authenticated():
		raise Http404#needs changes i thinl so
	#instance=get_object_or_404(post,id=id)
	try:
		instance=get_object_or_404(post,id=id)
	except:
		raise Http404
	if instance.user != request.user:
		response = HttpResponse("you do not have permission")
		response.status_code = 403
		return response
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context= {
		"title":instance.title,
		"instance":instance,
		"form":form,

		}
	return render(request, "forms.html", context)





#def signup(request):
#    #contact_list = Contacts.objects.all()
#    if request.method == 'POST':
#    	form = UserCreationForm(request.POST)
#    	if form.is_valid():
#    		form.save()
#    		username = form_cleaned_data['username']
#    		password = form_cleaned_data['password']
#    		user = authenticate(username=username,password=password)
#    		login(request,user)
#    		return redirect('/posts')
#
