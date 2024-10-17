from django.urls import path
from .views import CustomRegisterView, CustomLoginView

urlpatterns = [
    path('registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
]