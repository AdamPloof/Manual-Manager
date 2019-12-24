import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Manual(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name='author', null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    tags = models.CharField(max_length=150)
    pub_date = models.DateTimeField('Date Published', auto_now_add=True)
    admin = models.ForeignKey(User, related_name='admin_of', null=True, on_delete=models.SET_NULL)
    last_update = models.DateTimeField('Last Update', null=True, auto_now=True)
    last_update_by = models.ForeignKey(User, related_name='updated_by', null=True, on_delete=models.SET_NULL)
    next_update = models.DateTimeField('Next Update Due', null=True)
    update_assigned_to = models.ForeignKey(User, related_name='assigned_to', null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField('Archived', default=False)

    folder = TreeForeignKey(
    'Directory',
    default=1,
    related_name='manuals',
    on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.title

    def next_update_due(self):
        return self.last_update + datetime.timedelta(days=90)
        

    def get_absolute_url(self):
        return reverse('manual-detail', kwargs={'pk': self.pk})

class Directory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    parent = TreeForeignKey(
    'self',
    null=True,
    blank=True,
    related_name='children',
    on_delete=models.CASCADE
    )
    
    class MPTTMeta:
        order_insertion_by: ['name']

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'

    def __str__(self):
        return self.name