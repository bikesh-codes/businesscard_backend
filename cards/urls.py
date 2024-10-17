from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessCardViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'cards', BusinessCardViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
  path('', include(router.urls)),
]
