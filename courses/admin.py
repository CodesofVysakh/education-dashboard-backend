from django.contrib import admin
from courses.models import Subject

# Register your models here.
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'duration', 'description' ]
    search_fields = ['id', 'name', 'duration', 'description' ]


admin.site.register(Subject)