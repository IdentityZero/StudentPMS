from rest_framework import serializers
from .models import DocumentTypes, StudentDocuments, StudentProfile
from Users.models import UsersProfile

class DocumentTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypes
        fields = ['id','document_type', 'description']

class UsersProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = UsersProfile
        fields = ['full_name']

class StudentProfileSerializer(serializers.ModelSerializer):
    profile = UsersProfileSerializer()

    class Meta:
        model = StudentProfile
        fields = ['profile']
class StudentDocumentsSerializer(serializers.ModelSerializer):
    SP = StudentProfileSerializer()
    SD_doc_type = DocumentTypesSerializer()

    class Meta:
        model = StudentDocuments
        fields = ['id', 'SP','SD_doc_type', 'SD_document', 'SD_date_uploaded', 'SD_comment']
