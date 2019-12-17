from django.utils.http import urlencode
from django.urls import reverse

from .models import Directory

def reverse_query(*args, **kwargs):
    # Add query string to the end of reverse URL
    # For redirecting to correct folder of index
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)

    if get:
        url += '?' + urlencode(get)

    return url

def valid_move_nodes(node):
    # Create a queryset that only includes valid targets for moving nodes
    current_dir = Directory.objects.get(pk=node.pk)
    exclude_dirs = current_dir.get_descendants(include_self=True)

    move_to_dirs = Directory.objects.exclude(parent__in=exclude_dirs)

    return move_to_dirs