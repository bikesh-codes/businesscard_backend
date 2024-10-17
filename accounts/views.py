from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView

from .serializers import CustomRegisterSerializer, CustomLoginSerializer

class CustomRegisterView(RegisterView):
  serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
  serializer_class = CustomLoginSerializer
  
  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = super().post(request, *args, **kwargs)

    user = User.objects.get(username=serializer.validated_data['username'])
    response.data['user'] = {
      'username': user.username,
      'email': user.email,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'address': user.address,
      'phone_number': user.phone_number,
    }
    return response