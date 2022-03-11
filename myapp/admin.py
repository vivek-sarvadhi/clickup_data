from email.headerregistry import Group
from django.contrib import admin
from myapp.models import CustomUser
from myapp.forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','email','clickup_id','user_type')
    form = CustomUserForm

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            if obj.user_type == 1:
                obj.is_superuser = True
            obj.is_staff = True
            obj.save()


admin.site.register(CustomUser, AuthorAdmin)
admin.site.unregister(Group)