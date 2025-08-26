from rest_framework import serializers

from apps.utils.customs import CustomException

from .models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        exclude = ("password",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    sms_code = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "sms_code")

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_sms_code(self, sms_code):
        verification_code = 123456
        if sms_code != verification_code:
            raise CustomException("Tasdiqlash kodi noto'g'ri.")
        return sms_code

    def create(self, validated_data):
        validated_data.pop("sms_code")
        return User.objects.create_user(**validated_data, role=User.Role.CLIENT)
