from django.shortcuts import render,redirect
from django.contrib.auth import (
	authenticate,
	login,
	logout,
	get_user_model,
	)
from .forms import loginform, userRegisterForm
# Create your views here.
def login_view(request):
	title = 'Login'
	nextp = request.GET.get('next')
	form = loginform(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		if nextp:
			return redirect(nextp)
		return redirect("/")
	return render(request,"login_view.html",{"form":form , "title":title})

def logout_view(request):
	logout(request)
	return redirect("/")
	return render(request,"login_view.html" ,{})
	

def register_view(request):
	title = 'Register'
	form=userRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request,new_user)
		return redirect("/")

	return render(request, "login_view.html", {"title":title, "form":form})
