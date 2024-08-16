from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Area
from .forms import CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupo'

    def get_areas(self, obj):
        return ', '.join([area.nombre for area in obj.areas.all()])
    get_areas.short_description = 'Áreas'

    list_display = ('username', 'first_name', 'last_name', 'email', 'get_groups', 'is_staff', 'get_areas')
    list_filter = ['username', 'groups']

    # Aquí agregamos el campo areas al fieldset de permisos
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if len(fieldsets) > 2:
            fieldsets = list(fieldsets)
            fieldsets[2] = (
                fieldsets[2][0],
                {'fields': [f for f in fieldsets[2][1]['fields'] if f not in ['is_superuser', 'user_permissions']] + ['areas']}
            )
        return tuple(fieldsets)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'is_staff':
            field.label = 'Habilitar acceso del usuario'
        return field

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Area)
