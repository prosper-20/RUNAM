from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from .models import Profile, Referral
from django.conf import settings

from accounts.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = User
        fields = ("email",)
        # fields = ("id", "username", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["email", "date_joined", "password", "password2"]
        extra_kwargs = {
            "password":{"write_only": True}
        }

    def save(self):
        user = User(
            email = self.validated_data["email"],
            
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Response": "Both passwords must macth"})
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError('Incorrect Credentials')

        
        user = authenticate(username=user.email, password=data['password'])
        print(user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials')


    # def validate(self, data):
    #     user = authenticate(**data)
    #     if user and user.is_active:
    #         return user
    #     raise serializers.ValidationError("Incorrect Credentials")


class ReferralSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Referral
        fields = ["user", "code"]

class ProfileSerializer(CustomUserSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    # user = CustomUserSerializer()
    my_referral_code = serializers.SerializerMethodField("get_code")
    username = serializers.SerializerMethodField("get_user_username")
    class Meta:
        model = Profile
        fields = ("username", "bio", "phone_number", "avatar", "location", "my_referral_code")

    def get_code(self, obj):
        return ReferralSerializer(Referral.objects.get(user=obj.user)).data
    
    def get_user_username(self, obj:Profile):
        return obj.username

    


    

class ProfileAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the avatar
    """

    class Meta:
        model = Profile
        fields = ("avatar",)





class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

