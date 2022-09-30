from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from datetime import datetime
from user.models import CustomUser, BlackListedToken


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, write_only=True)
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def validate(self, attrs):
        if attrs["password1"] == attrs["password2"]:
            return attrs
        else:
            raise serializers.ValidationError("Please enter matched password!")

    def create(self, validated_data):
        password = validated_data["password1"]
        return CustomUser.objects.create_users(**validated_data, password=password)


class GetUsers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class SignUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    token = TokenSerializer(read_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login Credential")
        else:
            refresh = RefreshToken.for_user(user)
            login_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
            }
            return login_data


class BlacklistTokenSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(write_only=True)

    class Meta:
        model = BlackListedToken
        fields = ['token', 'created_at']


class SignOutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs["refresh"])
            token.blacklist()
            token_data = {
                'token': attrs['token'],
                'created_at': datetime.date(datetime.today())
            }
            token_blacklist = BlacklistTokenSerializer(data=token_data)
            token_blacklist.is_valid(raise_exception=True)
            token_blacklist.save()
        except TokenError:
            raise serializers.ValidationError("token is invalid")
        return attrs


class ChangeUserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        password = attrs["current_password"]
        password1 = attrs["new_password1"]
        password2 = attrs["new_password2"]
        email = attrs["email"]
        if authenticate(email=email, password=password):
            if password1 != password2:
                raise serializers.ValidationError("Password does not match")
            else:
                user = CustomUser.objects.get(email=email)
                user.set_password(password1)
                user.save()
                return attrs
        else:
            raise serializers.ValidationError("Please enter correct current password")
