from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CandidateProfile, JobRole, ProfessionalReference, WorkExperience


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ("id", "name")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        CandidateProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ("profile",)


class ProfessionalReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalReference
        exclude = ("profile",)


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    experiences = WorkExperienceSerializer(many=True, read_only=True)
    references = ProfessionalReferenceSerializer(many=True, read_only=True)
    personal_photo = serializers.ImageField(required=False, allow_null=True)
    personal_photo_url = serializers.SerializerMethodField()
    role = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all(), required=False, allow_null=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    def validate(self, attrs):
        role = attrs.get("role")
        if role is None and self.instance and self.instance.role_id:
            role = self.instance.role

        if role is None:
            raise serializers.ValidationError({"role": "Debes seleccionar un rubro."})

        return attrs

    def get_personal_photo_url(self, obj):
        if not obj.personal_photo:
            return ""

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.personal_photo.url)
        return obj.personal_photo.url

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "personal_photo",
            "personal_photo_url",
            "phone",
            "city",
            "role",
            "role_name",
            "years_experience",
            "availability",
            "bio",
            "experiences",
            "references",
        )
