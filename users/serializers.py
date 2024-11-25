from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            attrs["access"] = str(token.access_token)
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token.")
        return attrs
