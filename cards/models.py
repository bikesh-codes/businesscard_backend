from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class BusinessCard(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business_card')
  name = models.CharField(max_length=255, db_index=True)
  title = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=20, validators=[
    RegexValidator(
      regex=r'^\+?1?\d{9,15}$',
      message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
  ])
  website = models.URLField(blank=True)
  social_links = models.JSONField(default=dict, blank=True)
  views = models.PositiveIntegerField(default=0)
  leads = models.PositiveIntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']
    indexes = [
      models.Index(fields=['name']),
      models.Index(fields=['email']),
    ]

  def __str__(self):
    return self.name
  
  def increment_views(self):
    self.views = F('views') + 1
    self.save(update_fields=['views'])

  def increment_leads(self):
    self.leads = F('leads') + 1
    self.save(update_fields=['leads'])


class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  bio = models.TextField(blank=True)
  profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

  def __str__(self):
      return self.user.username


class EngagementLog(models.Model):
  ACTION_CHOICES = [
    ('viewed', 'Viewed'),
    ('lead', 'Lead'),
  ]

  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='engagements')
  card = models.ForeignKey(BusinessCard, on_delete=models.CASCADE, related_name='engagements')
  action = models.CharField(max_length=10, choices=ACTION_CHOICES)
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    indexes = [
      models.Index(fields=['user', 'card', '-timestamp']),
    ]

  def __str__(self):
      return f"{self.user.username} {self.action} on {self.card.name} at {self.timestamp}"
   
   

  
