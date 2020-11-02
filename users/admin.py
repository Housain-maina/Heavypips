from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'allowaccess')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser','is_signalmanager', 'is_newslettermanager', 'is_active',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'birth_date', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'is_staff', 'is_superuser', 'allowaccess', 'is_signalmanager', 'is_newslettermanager',)
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'birth_date','is_staff', 'is_superuser', 'allowaccess', 'is_signalmanager', 'is_newslettermanager', )
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)
