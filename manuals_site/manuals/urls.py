from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cd/', views.index, name='index-ajax'),
    path('manual/new-folder', views.DirectoryCreate.as_view(), name='dir-create'),
    path('manual/<int:pk>/update-folder', views.DirectoryUpdate.as_view(), name='dir-update'),
    path('manual/<int:pk>/delete-folder', views.DirectoryDelete.as_view(), name='dir-delete'),
    path('manual/<int:pk>/', views.ManualDetail.as_view(), name='manual-detail'),
    path('manual/new', views.ManualCreate.as_view(), name='manual-create'),
    path('manual/<int:pk>/update/', views.ManualUpdate.as_view(), name='manual-update'),
    path('manual/<int:pk>/delete/', views.ManualDelete.as_view(), name='manual-delete'),   
]
