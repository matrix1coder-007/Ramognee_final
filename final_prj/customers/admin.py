from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from customers.models import CustomUserModel

admin.site.unregister(Group)


class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['user_fullname', 'user_email']

    fieldsets = (
        ('Personal Details', {
            'fields': (
                'user_email',
                'fname_user',
                'mname_user',
                'lname_user',
                'password'
            ),
        }),
        ('Official Details',
         {
             'fields': (
                 'joining_dt_user',
                 'deactivation_dt_user',
                 'admin',
                 'staff',
             ), }),

    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(CustomUserModel, CustomUserModelAdmin)
