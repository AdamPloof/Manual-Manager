from django.utils.http import urlencode
from django.urls import reverse

from .models import Directory, Department, Manual


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
    dept = scan_manuals_for_department(node)
    if dept:
        return dept

    siblings = node.get_siblings(include_self=False)
    for folder in siblings:
        dept = scan_manuals_for_department(folder)
        if dept:
            return dept
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


def get_assignment_count(user):
    # Retrieve counts for current users total assigned manuals as well as
    # counts for each update status of those manuals

    if not user.is_authenticated:
        # Check if user is logged in and if not return 0 assignments
        counts = {
            'assigned_count': 0,
            'overdue_count': 0,
            'due_soon_count': 0,
            'current_count': 0
        }
        return counts

    assigned = user.assigned_to(manager='active_objects').all()

    assigned_count = 0
    overdue_count = 0
    due_soon_count = 0
    current_count = 0

    for manual in assigned:
        if manual.update_status() == "overdue":
            overdue_count += 1
            assigned_count += 1
        elif manual.update_status() == "due_soon":
            due_soon_count += 1
            assigned_count += 1
        else:
            current_count += 1
            assigned_count += 1

    counts = {
        'assigned_count': assigned_count,
        'overdue_count': overdue_count,
        'due_soon_count': due_soon_count,
        'current_count': current_count
    }
    
    return counts