from rest_framework import serializers

from activity.models import Enrollment


class EnrollmentListSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    student_username = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = (
            'id', 
            'student_name', 
            'courses', 
            'enrollment_time', 
            'student_username'
        )

    def get_courses(self, instance):
        return [course.name for course in instance.courses.all()]
    
    def get_student_username(self, instance):
        return instance.student_username.id


class EnrollSerializer(serializers.Serializer):
    course = serializers.CharField()
    student_id = serializers.CharField();

class EnrolledSerializer(serializers.Serializer):
    student_id = serializers.CharField();