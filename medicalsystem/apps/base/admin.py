from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupo'  # Define el nombre de la columna en el admin

    list_display = ('username', 'first_name', 'last_name', 'email', 'get_groups', 'is_staff')  # Agregar 'get_groups'

    def get_fieldsets(self, request, obj=None):
        # Copia los fieldsets predeterminados
        fieldsets = super().get_fieldsets(request, obj)
        # Verifica si fieldsets tiene al menos un conjunto de campos
        if len(fieldsets) > 2:
            # Remueve los campos 'is_superuser' y 'user_permissions' del segundo conjunto de campos (índice 2)
            fieldsets = list(fieldsets)
            fieldsets[2] = (
                fieldsets[2][0],
                {'fields': [f for f in fieldsets[2][1]['fields'] if f not in ['is_superuser', 'user_permissions']]}
            )
        return tuple(fieldsets)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'is_staff':
            field.label = 'Habilitar acceso del usuario'
        return field

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
