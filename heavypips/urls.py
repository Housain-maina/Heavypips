"""heavypips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_view
from users.forms import UserLoginForm, MyPasswordResetForm, MyPasswordChangeForm


urlpatterns = [
    path('', include('signalsection.urls')),
    path('secretadmin/', admin.site.urls),
    path('register/', users_view.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
                                                                 form_class=MyPasswordResetForm,
                                                                 from_email='passwordreset@heavypips.com',
                                                                 email_template_name='users/password_reset_email.html'),
         name='password-reset'),
    path('password-reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html',
                                                                   form_class=MyPasswordChangeForm),
         name='password-change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('contact-us/', users_view.ContactView, name='contact'),
    path('settings/', users_view.settings, name='settings'),
    path('activate-account/<uidb64>/<token>/', users_view.activate, name='activate-account'),
]
