from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
  first_name = serializers.CharField(required=True)
  last_name = serializers.CharField(required=True)
  address = serializers.CharField(required=True)
  phone_number = serializers.CharField(required=True)
  
  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("Email is already in use.")
    return value
  
  def validate_username(self, value):
    if User.objects.filter(username=value).exists():
      raise serializers.ValidationError("Username is already in use.")
    return value
  
  def validate_phone_number(self, value):
    if User.objects.filter(phone_number=value).exists():
      raise serializers.ValidationError("Phone number is already in use.")
    return value

  def save(self, **kwargs):
    user = super().save(**kwargs)
    user.first_name = self.validated_data.get('first_name')
    user.last_name = self.validated_data.get('last_name')
    user.address = self.validated_data.get('address')
    user.phone_number = self.validated_data.get('phone_number')
    user.save()
    return user
  

class CustomLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()
  
  def validate(self, attrs):
    user = User.objects.filter(username=attrs['username']).first()
    if user is None:
      raise serializers.ValidationError("User not found.")
    
    if not user.check_password(attrs['password']):
      raise serializers.ValidationError("Incorrect password.")
    
    if not user.is_active:
      raise serializers.ValidationError("User account is inactive")
    
    return attrs