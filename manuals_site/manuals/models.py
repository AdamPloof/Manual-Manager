import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Manual(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    tags = models.CharField(max_length=150)
    pub_date = models.DateTimeField('Date Published', auto_now_add=True)
    last_update = models.DateTimeField('Last Update', auto_now=True)
    is_archived = models.BooleanField(default=False)

    folder = TreeForeignKey(
    'Directory',
    default=1,
    related_name='manuals',
    on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.title

    def next_update_due(self):
        now = timezone.now()
        return last_update + datetime.timedelta(days=90)

    def get_absolute_url(self):
        return reverse('manual-detail', kwargs={'pk': self.pk})

class Directory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
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