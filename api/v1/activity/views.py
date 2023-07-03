from uuid import UUID
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

from accounts.models import Profile
from courses.models import Subject
from activity.models import Enrollment
from api.v1.activity.serializers import EnrollSerializer, EnrollmentListSerializer, EnrolledSerializer
from general.functions import generate_serializer_errors


@api_view(['POST'])
@permission_classes([AllowAny])
def enroll_subject(request):
    serialized = EnrollSerializer(data=request.data)

    if serialized.is_valid():
        course_id = request.data['course']
        student_username = request.data['student_id']

        if Profile.objects.filter(id=student_username, is_deleted=False).exists():
            profile = Profile.objects.get(id=student_username, is_deleted=False)

            if Subject.objects.filter(id=course_id, is_deleted=False).values_list('id', flat=True).exists():
                course_ids = Subject.objects.filter(id=course_id, is_deleted=False).values_list('id', flat=True)

                enrollment = Enrollment.objects.filter(
                            student_name=profile.name,
                            student_username=student_username,
                            is_deleted=False
                        ).first();

                if enrollment:

                    enrollment.courses.add(*course_ids)

                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "Courses added to existing enrollment list",
                            "id": enrollment.id,
                            "student_name": enrollment.student_name,
                            "student_username": enrollment.student_username.name,
                            "courses": [course.name for course in enrollment.courses.all()],
                        }
                    }
                else:

                    enroll = Enrollment.objects.create(
                        student_name=profile.name,
                        student_username=profile,
                    )
                    enroll.courses.set(course_ids)

                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "Successfully enrolled in subject",
                            "id": enroll.id,
                            "student_name": enroll.student_name,
                            "student_username": enroll.student_username.name,
                            "courses": [course.name for course in enroll.courses.all()],
                        }
                    }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Subject not found",
                        "message": "Please provide correct subject ID"
                    }
                }
        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Profile not found",
                    "message": "Please signup for enrolling"
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def enrollment_list(request):
    instances = Enrollment.objects.filter(is_deleted=False)

    serialized = EnrollmentListSerializer(
        instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "message": "Successfully listed all enrollments",
            "data": serialized.data,
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def student_enrolled_list(request):
    serialized = EnrolledSerializer(data=request.data)

    if serialized.is_valid():
        student_id = request.data['student_id']
        instances = Enrollment.objects.filter(student_username=student_id,is_deleted=False).first()

        if instances:
            course_id = [course.id for course in instances.courses.all()]
        else:
            course_id = ""

        response_data = {
            "StatusCode": 6000,
            "data": {
                "message": "Successfully listed all enrollments",
                "data": course_id,
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def dashboard_list(request):
    serialized = EnrolledSerializer(data=request.data)

    if serialized.is_valid():
        student_id = request.data['student_id']

        instances = Enrollment.objects.filter(is_deleted=False)
        student = Profile.objects.filter(role="student", is_deleted=False)
        subject = Subject.objects.all()

        enrollment = Enrollment.objects.filter(
                            student_username=student_id,
                            is_deleted=False
                        ).first();
        if enrollment:
            course_names = [course.name for course in enrollment.courses.all()]
        else:
            course_names = ""

        # enrollments_count = Enrollment.objects.filter(courses__in=subject).values('name').annotate(count=Count('name'))

        # print(subject, "@@@@@@@@@@@@@@@@@", enrollments_count)

        serialized = EnrollmentListSerializer(
            instances, many=True, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "data": {
                "message": "Successfully listed all enrollments",
                "enrollment_count" : len(instances),
                "student_count" : len(student),
                "courses": course_names,
                # "enrolled_subjects": total_enrollments
                # "subject_count": len(enrollments_count),
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def admin_dashboard_list(request):

    instances = Enrollment.objects.filter(is_deleted=False)
    student = Profile.objects.filter(role="student", is_deleted=False)
    subject = Subject.objects.all()

    # print(total_enrollments, "@@@@@@@@@@@@@@@@@@")


    # enrollments_count = Enrollment.objects.filter(courses__in=subject).values('name').annotate(count=Count('name'))

    # print(subject, "@@@@@@@@@@@@@@@@@", enrollments_count)

    serialized = EnrollmentListSerializer(
        instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "message": "Successfully listed all enrollments",
            "enrollment_count" : len(instances),
            "student_count" : len(student),
            # "enrolled_subjects": total_enrollments
            # "subject_count": len(enrollments_count),
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)