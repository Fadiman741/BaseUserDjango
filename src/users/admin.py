from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
# In your app's admin.py or any admin.py file that loads after allauth's
from allauth.socialaccount.admin import SocialAppAdmin, SocialTokenAdmin, SocialAccountAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff','occupation', 'profile_picture',
                'role', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone')
    search_fields = ('username', 'email', 'first_name', 'last_name','date_joined', 'is_staff','occupation', 'profile_picture',
                'role',  'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone'  )
    readonly_fields = ('date_joined',)

admin.site.register(User, CustomUserAdmin)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)

# Then re-register if you need custom admin classes
admin.site.register(SocialApp, SocialAppAdmin)
admin.site.register(SocialToken, SocialTokenAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)