from django.contrib import admin


# Register your models here.

from datetime import datetime

from .models import IncidentModel

from customers.models import CustomUserModel



class IncidentModelAdmin(admin.ModelAdmin):

    readonly_fields = []
    list_display = ['created_at', 'author_name', 'priority', 'status', '__str__']
    search_fields = ['incident_id']


    def save_model(self, request, obj, form, change):

        author_email = request.user
        obj.fk_user_uuid = CustomUserModel.objects.filter(user_email=author_email).first()
        
        if obj.status=='Closed':
            obj.close_date = datetime.now()
            self.readonly_fields.append('incident_details')

        super().save_model(request, obj, form, change)



    def author_name(self, obj):


        author_obj = CustomUserModel.objects.filter(user_email=obj.fk_user_uuid).first()


        if author_obj:

            first_name = author_obj.fname_user if author_obj.fname_user else ''

            mid_name = author_obj.mname_user if author_obj.mname_user else ''

            last_name = author_obj.lname_user if author_obj.lname_user else ''

            return first_name + ' ' + mid_name + ' ' + last_name
            

        else:

            return '-'


    fieldsets = (


        ('Incident Details', {

            'fields': (

                'priority',
                'status',
                'incident_details',
                'close_date'
            ),

        }),
    )


    def get_queryset(self, request):
        

        qs = super().get_queryset(request)


        if request.user.is_superuser:

            return qs

        else:

            authenticated_author = CustomUserModel.objects.filter(user_email=request.user).values('uuid_user')[0]['uuid_user']

            return qs.filter(fk_user_uuid_id=authenticated_author)


    # def field_has_changed(self, obj):


    #     print('obj-status', obj.status)


    #     if obj.status=='CLOSED':

    #         obj.close_date = datetime.datetime()

    #     super().save_model(request, obj, form, change)



admin.site.register(IncidentModel, IncidentModelAdmin)

