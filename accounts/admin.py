from django.contrib import admin
from accounts.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'password', 'dob', 'phone', 'name' ]
    search_fields = ['id', 'username', 'email', 'password', 'dob', 'phone', 'name' ]


admin.site.register(Profile)