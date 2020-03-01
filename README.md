# Manual-Manager
A Django app for collecting, organizing and maintaining procedure manuals.

**Manual Manager** is a Django application for creating, organizing and maintaining manuals within an organization.
The structure is similar to a document manager with a directory tree and files, but with a few extra features intended to
help maintain documents. The primary method for this is that each manual is associated with an admin. Admins are responsible
for assigning updates to other users as well as adjusting due dates and archiving manuals that are no longer needed. Users can
view documents that they've authored, updated, been assigned and have admin responsibility for.

## Key Features
* WYSIWYG editor for creating and updating manuals
* Image upload incorporated into the editor
* Automatic reminders of overdue and due soon documents
* Favorites options for quick navigation
* Add, delete, move, rename directories
* When creating new documents, Admins are automatically determined based on the admin assignment of adjacent docs.
This can be changed from the django-admin
* Next-Update-Due automatically adjusted when manuals are created and updated.
* Alerts and contextual formatting for documents that require attention
* Search functionality

# Improvements to be made
* Fix bug where directories are not always assigned the intended parent.
* Add draft feature
