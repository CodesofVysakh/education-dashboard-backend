from django.urls import path

from api.v1.courses import views


app_name = "api_v1_courses"


urlpatterns = [
    path('list-subjects/', views.course_list),
    path('add-subject/', views.add_subject),
    path('delete-subject/', views.delete_subject),
]