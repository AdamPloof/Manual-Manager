import re

from django.db.models.signals import post_save, post_delete
from .models import Directory, Manual
from django.dispatch import receiver


@receiver(post_save, sender=Directory)
def create_node(sender, instance, created, **kwargs):
    if created:
        Directory.objects.rebuild()
        print('Tree rebuilt')


@receiver(post_save, sender=Directory)
def update_node(sender, instance, **kwargs):
    Directory.objects.rebuild()
    print('Tree rebuilt')


@receiver(post_delete, sender=Directory)
def delete_node(sender, instance, **kwargs):
    Directory.objects.rebuild()
    print('Tree rebuilt')


@receiver(post_save, sender=Manual)
def set_manual_admin(sender, instance, created, **kwargs):
    if created:
        department = instance.department
        managers = department.manager.all()

        for manager in managers:
            instance.admin.add(manager)
        
        instance.save()


@receiver(post_save, sender=Manual)
def correct_img_src(sender, instance, created, **kwargs):
    # Correct the the src attribute of images when manuals are created
    # A workaround for a bug in the way File Uploader seems to handle images
    if created:
        p = re.compile("<img src=\"../media/uploads/")
        content = instance.content
        corrected_content = p.sub("<img src=\"../../../media/uploads/", content)
        instance.content = corrected_content
        instance.save()