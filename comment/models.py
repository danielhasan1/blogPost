from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models

# Create your models here.
class commentmanager(models.Manager):
    def all(self):
        qs = super(commentmanager ,self).filter(parent=None)
        return qs
    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(commentmanager,self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        #comments = comment.objects.filter(content_type=content_type, object_id=obj_id)
        return qs

class comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = models.ForeignKey("self",null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects=commentmanager()

    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
    	return str(self.user.username)

    def children(self):
        return comment.objects.filter(parent = self)
    

    def get_absolute_url(self):
        return reverse("comment:thread", kwargs={"id":self.id})
    
    def get_delete_url(self):
        return reverse("comment:delete",kwargs={"id":self.id})

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True