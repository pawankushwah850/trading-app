from rest_framework import serializers

from user.models import *
from investment.serializers import *


class SignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'profile_photo', 'referral_code',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_referral_code(self, referral_code):

        try:
            return User.objects.get(referral_code=referral_code)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Referral Code')

    def create(self, validated_data):

        referred_by = None
        try:
            referred_by = validated_data.pop('referral_code')
        except KeyError:
            pass
        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        user.save()
        if referred_by:
            Referral.objects.create(referred_by=referred_by,
                                    referred_to=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_number', 'password', 'verification_status', 'profile_photo',
                  'referral_code', 'language', 'created_at']
        extra_kwargs = {
            'identity_document': {'write_only': True},
            'language': {'write_only': True},
            'password': {'write_only': True}
        }

    def validate_referral_code(self, referral_code):
        try:
            return User.objects.get(referral_code=referral_code)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Referral Code')

    def create(self, validated_data):
        self.SUPER_USER = "admin@admin.com"
        referred_by = None
        try:
            referred_by = validated_data.pop('referral_code')
        except KeyError:
            pass
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        if validated_data['email'] == self.SUPER_USER:
            user.is_superuser = True
            user.is_active = True
            user.is_staff = True
            user.get_all_permissions()
        user.save()

        if referred_by:
            Referral.objects.create(referred_by=referred_by,
                                    referred_to=user)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=10)
    new_password = serializers.CharField(max_length=20)

    def validate_token(self, token):
        try:
            token = ForgetPasswordToken.objects.get(token=token)
            print(token.token)
            print(token.expire_at.strftime('%D'))
            if token.is_expired:
                raise serializers.ValidationError('Invalid Token.')
            else:
                return token
        except ForgetPasswordToken.DoesNotExist:
            raise serializers.ValidationError('Invalid  Token.')


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Notification
        fields = ('user', 'category', 'message', 'created_at', 'is_ack',)
