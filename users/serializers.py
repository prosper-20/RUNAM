from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from .models import Profile, Referral
User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = User
        fields = ("username", "email")
        # fields = ("id", "username", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["username", "email", "date_joined", "password", "password2"]
        extra_kwargs = {
            "password":{"write_only": True}
        }

    def save(self):
        user = User(
            email = self.validated_data["email"],
            username = self.validated_data["username"]
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
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


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

    class Meta:
        model = Profile
        fields = ("bio", "phone_number", "my_referral_code")

    def get_code(self, obj):
        return ReferralSerializer(Referral.objects.get(user=obj.user)).data

    


    

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

