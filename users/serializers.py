from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Order, Product


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'user_image']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bio']

class UserPutPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'user_image']


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password']

    def validate(self, attrs):
        user = self.context['request'].user

        # Verify the current password
        current_password = attrs.get('current_password')
        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")

        new_password = attrs.get('new_password')
        if current_password == new_password:
            raise ValidationError("New password cannot be the same as the current password.")

        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']

        # Update the user's password
        user.set_password(new_password)
        user.save()

        return user



class LastOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class RecentOrdersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    product_name = serializers.CharField(source='product.name')
    class Meta:
        model = Order
        fields = ('created_at', 'price', 'username', 'product_name')

class TopProductSerializer(serializers.ModelSerializer):
    total_sold = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'total_sold']