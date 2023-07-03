import requests
import json
from django.conf import settings as SETTINGS
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from general.functions import generate_serializer_errors, get_auto_id, generate_unique_id

from accounts.models import Profile
from api.v1.accounts.serializers import ProfileSerializer, JoinSerializer, RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serialized = JoinSerializer(data=request.data)

    if serialized.is_valid():
        email = request.data['email']
        password = request.data['password']

        if Profile.objects.filter(email=email, password=password, is_deleted=False).exists():
            profile = Profile.objects.get(email=email, password=password, is_deleted=False)
            
            response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "successful login",
                            "email" : email,
                            "name" : profile.name,
                            "dob" : profile.dob,
                            "username" : profile.username,
                            "id" : profile.id,
                            "role" : profile.role,
                            "is_verified": True, 
                        }
                    }
        else:
            response_data = {
                "StatusCode": 6001,
                "title": "Invalid request",
                "message": "Please check credentials or Sign up",
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
def register(request):
    serialized = RegisterSerializer(data=request.data)

    if serialized.is_valid():
        email = request.data['email']
        password = request.data['password']
        name = request.data['name']

        try:
            phone = request.data['phone']
            dob = request.data['dob']
        except:
            phone = ''
            dob = ''

        if not Profile.objects.filter(email=email, name=name, is_deleted=False).exists():

            complete_username = generate_unique_id(size=20)

            username_duplicate = User.objects.filter(username=complete_username).exists()

            while username_duplicate:
                complete_username = generate_unique_id(size=20)
                username_duplicate = User.objects.filter(username=complete_username).exists()

            user = User.objects.create_user(
                username=complete_username,
                password=password
            )
            
            profile = Profile.objects.create(
                user=user,

                email=email,
                password=password,
                name=name,
                dob=dob,
                phone=phone,
                username=f"EC{str(user.pk).zfill(6)}"
            )

            profile.save()

            response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "successfully registered",
                            "email" : profile.email,
                            "name" : profile.name,
                            "username" : profile.username,
                            "id" : profile.id,
                            "phone" : profile.phone,
                            "dob" : profile.dob,
                            "role" : profile.role,
                            "is_verified": True, 
                        }
                    }
        else:
            response_data = {
                "StatusCode": 6001,
                "title": "Invalid request",
                "message": "Already registered.",
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
def student_list(request):
    instances = Profile.objects.filter(role="student", is_deleted=False)
    serialized = ProfileSerializer(
        instances, many=True, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": {
            "message": "Successfully listed all students",
            "data": serialized.data,
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)