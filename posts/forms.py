from django import forms
from pagedown.widgets import PagedownWidget
from . models import post

class PostForm(forms.ModelForm):
	content = forms.CharField(widget = PagedownWidget(show_preview=False))
	publish = forms.DateField(widget = forms.SelectDateWidget)
	class Meta:
		model = post
		fields=[
		"title",
		"markdown",
		"content",
		"image",
		"draft",
		"publish",
		]
