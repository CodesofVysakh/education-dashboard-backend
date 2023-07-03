from rest_framework import serializers

from courses.models import Subject


class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'duration',
            'description',
        )

class AddSubjectSerializer(serializers.Serializer):
    name = serializers.CharField();
    duration = serializers.CharField()
    description = serializers.CharField();

class RemoveSubjectSerializer(serializers.Serializer):
    subject_id = serializers.CharField();