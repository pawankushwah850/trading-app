from rest_framework import serializers
from user.models import User, Referral
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_number', 'password', 'verification_status', 'profile_photo',
                  'referral_code', 'language']
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
        referred_by = None
        try:
            referred_by = validated_data.pop('referral_code')
        except KeyError:
            pass
        user = super().create(validated_data)
        user.password = make_password(validated_data.get('password', '1234'))
        if referred_by:
            Referral.objects.create(referred_by=referred_by,
                                    referred_to=user)
        return user
