from rest_framework import serializers
from .models import BusinessCard, UserProfile


class BusinessCardSerializer(serializers.ModelSerializer):
  class Meta:
    model = BusinessCard
    fields = ['id', 'user', 'name', 'title', 'email', 'phone', 'website', 'social_links', 'views', 'leads']
    read_only_fields = ['views', 'leads', 'created_at', 'updated_at']

  def validate_email(self, value):
    if BusinessCard.objects.filter(email=value).exists():
      raise serializers.ValidationError("Email is already in use.")
    return value
  

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['id', 'user', 'bio', 'profile_picture']