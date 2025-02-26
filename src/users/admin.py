from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff','occupation', 'profile_picture',
                'role', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone')
    search_fields = ('username', 'email', 'first_name', 'last_name','date_joined', 'is_staff','occupation', 'profile_picture',
                'role',  'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone'  )
    readonly_fields = ('date_joined',)

admin.site.register(User, CustomUserAdmin)



