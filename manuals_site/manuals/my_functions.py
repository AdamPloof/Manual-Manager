from django.utils.http import urlencode
from django.urls import reverse

from .models import Directory, Department


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

    move_to_dirs = Directory.objects.exclude(parent__in=exclude_dirs).exclude(pk=current_dir.pk)

    return move_to_dirs


def scan_manuals_for_department(node):
    # returns department of first manual found in directory or None if no department is found
    manual_set = node.manuals.all()

    if manual_set:
        for manual in manual_set:
            if manual.department:
                department = manual.department
                return department
    else:
        # No manuals in current directory
        return None

    # No manuals were found in the manual_set that had a department associated    
    return None


def get_default_department(node):
    # Identify a likely default department when creating new manuals
    # Check current directory, then siblings, then ancestors
    # Use the department of the manuals contained as default for new manual
    siblings = node.get_siblings(include_self=True)
    for node in siblings:
        department = scan_manuals_for_department(node)
        if department:
            return department
        else:
            pass

    if node.pk != 1:
        # If no department is found in current dir or its siblings
        # Check the parent dir with a recursive call
        parent = node.parent
        return get_default_department(parent)
    else:
        # All ancestors have been checked for manuals with departments assigned
        # Time to give up and return None
        return None