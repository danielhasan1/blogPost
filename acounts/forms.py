from django import forms
from django.contrib.auth import (
	authenticate,
	login,
	logout,
	get_user_model,
	)
User = get_user_model()
class loginform(forms.Form):
	username = forms.CharField()
	#password1 = forms.CharField(widget=forms.PasswordInput)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self ,*args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		password1 = self.cleaned_data.get("password1")
		
		#user_qs = User.objects.filter(username=username)
		#if user_qs.count == 1:
		#	user=user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exits")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(loginform , self).clean(*args, **kwargs)


class userRegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(label='Email Address')
	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'password',
		'password1',
		
		]


	def clean_password1(self):
		
		pass1 = self.cleaned_data.get('password')
		pass2 = self.cleaned_data.get('password1')
		email = self.cleaned_data.get('email')
		
		if pass1 != pass2:
			raise forms.ValidationError("password must match!")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This Email has already been registerd")
		return pass1