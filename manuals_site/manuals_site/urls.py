from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('', include('manuals.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name='profile' ),
    path('profile/favorites/', user_views.manage_favs, name='favorites'),
    path('profile/preferences/', user_views.preferences, name='preferences'),
    path('profile/<int:pk>/change-image/', user_views.ProfileUpdateImageView.as_view(), name='change_image'),
    path('profile/favorites/update/', user_views.profile_add_fav, name='fav-update'),
    path('profile/favorites/remove/', user_views.profile_remove_fav, name='fav-remove'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ALLOW_USER_FIELD_UPDATES:
    # In case there's ever a need to update fields on the User model:
    urlpatterns.append(path('user/<int:pk>/update/', user_views.UserUpdateView.as_view(), name='user_update'))