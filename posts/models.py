from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings
from markdown_deux import markdown
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from comment.models import comment

class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())
# Create your models here.
class post(models.Model):
	title=models.CharField(max_length=120)
	content=models.TextField()
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	draft=models.BooleanField(default=False)
	markdown=models.BooleanField(default=False)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	image=models.FileField(null=True,blank=True)
	update=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

	objects = PostManager()
	def __str__(self):
		return self.title
	@property
	def get_content_type(self):
		instance=self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


	@property
	def comments(self):
		instance=self
		qs = comment.objects.filter_by_instance(instance)
		return qs


	def get_markdown(self):
		content=self.content
		return mark_safe(markdown(content))


	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id": self.id})
