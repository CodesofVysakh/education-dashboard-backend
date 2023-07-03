from django.urls import path

from api.v1.accounts import views


app_name = "api_v1_accounts"


urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('student-list/', views.student_list),
]