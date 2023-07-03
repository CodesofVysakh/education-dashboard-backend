from django.contrib import admin
from django.urls import path
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/accounts/', include('api.v1.accounts.urls', namespace='api_v1_accounts')),
    path('api/v1/courses/', include('api.v1.courses.urls', namespace='api_v1_courses')),
    path('api/v1/activity/', include('api.v1.activity.urls', namespace='api_v1_activity')),
]
