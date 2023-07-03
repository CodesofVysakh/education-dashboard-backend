from django.urls import path

from api.v1.activity import views


app_name = "api_v1_activity"


urlpatterns = [
    path('subject-enroll/', views.enroll_subject),
    path('enrollment-list/', views.enrollment_list),
    path('student-enrolled-list/', views.student_enrolled_list),
    path('dashboard-list/', views.dashboard_list),

    path('admin-dashboard-list/', views.admin_dashboard_list),
]