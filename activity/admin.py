from django.contrib import admin
from activity.models import Enrollment

# Register your models here.
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_name', 'courses', 'enrollment_time', 'student_username' ]
    search_fields = ['id', 'student_name', 'courses', 'enrollment_time', 'student_username' ]


admin.site.register(Enrollment)