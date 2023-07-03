from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from courses.models import Subject
from api.v1.courses.serializers import SubjectListSerializer, AddSubjectSerializer, RemoveSubjectSerializer
from general.functions import generate_serializer_errors

@api_view(['GET'])
@permission_classes([AllowAny])
def course_list(request):
    instances = Subject.objects.filter(is_deleted=False)
    serialized = SubjectListSerializer(
        instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "message": "Successfully listed all subjects",
            "data": serialized.data,
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_subject(request):
    serialized = AddSubjectSerializer(data=request.data)

    if serialized.is_valid():
        name = request.data['name']
        duration = request.data['duration']
        description = request.data['description']

        if not Subject.objects.filter(name=name, is_deleted=False).exists():
            subject = Subject.objects.create(
                name=name, 
                duration=duration, 
                description=description
            )
            
            subject.save()

            response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "successfully created subject",
                            "id" : subject.id,
                            "name" : subject.name,
                            "duration" : subject.duration,
                            "description" : subject.description,
                        }
                    }
        else:
            response_data = {
                "StatusCode": 6001,
                "title": "Invalid request",
                "message": "Subject with name already exists",
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
def delete_subject(request):
    serialized = RemoveSubjectSerializer(data=request.data)

    if serialized.is_valid():
        subject_id = request.data['subject_id']

        if Subject.objects.filter(id=subject_id, is_deleted=False).exists():
            subject = Subject.objects.filter(id=subject_id, is_deleted=False)
            
            for item in subject:
                item.is_deleted = True
                item.save()
                

            response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "successfully deleted subject"
                        }
                    }
        else:
            response_data = {
                "StatusCode": 6001,
                "title": "Invalid request",
                "message": "Subject does not exists",
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



