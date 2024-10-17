from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import BusinessCard, UserProfile, EngagementLog
from .serializers import BusinessCardSerializer, UserProfileSerializer
import qrcode
from django.http import HttpResponse
from io import BytesIO


class BusinessCardViewSet(viewsets.ModelViewSet):
  queryset = BusinessCard.objects.all()
  serializer_class = BusinessCardSerializer
  permission_classes = [permissions.IsAuthenticated]
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_fields = ['name', 'title']
  search_fields = ['name', 'title', 'email']
  ordering_fields = ['name', 'views', 'leads', 'created_at']

  def get_queryset(self):
    if self.action in ['list', 'retrieve']:
      return BusinessCard.objects.all()
    return BusinessCard.objects.filter(user=self.request.user)

  @action(detail=True, methods=['get'])
  def view_card(self, request, pk=None):
    card = self.get_object()
    card.increment_views()

    EngagementLog.objects.create(
      user=request.user, 
      card=card, 
      action='viewed'
    )
    serializer = self.get_serializer(card)
    return Response(serializer.data)
  
  @action(detail=True, methods=['get'])
  def generate_lead(self, request, pk=None):
    card = self.get_object()
    card.increment_leads()
    EngagementLog.objects.create(
      user=request.user, 
      card=card, 
      action='lead'
    )
    return Response({'leads': card.leads})
  
  @action(detail=True, methods=['get'])
  def qr_code(self, request, pk=None):
    card = self.get_object()
    card_url = f"https://yourdomain.com/cards/{card.id}/"
    
    try:
      img = qrcode.make(card_url)
      buffer = BytesIO()
      img.save(buffer, format='PNG')
      buffer.seek(0)
      return HttpResponse(buffer, content_type='image/png')
    except Exception as e:
      return Response(
        {'error': 'Failed to generate QR code'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
     

class UserProfileViewSet(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer

  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
    
