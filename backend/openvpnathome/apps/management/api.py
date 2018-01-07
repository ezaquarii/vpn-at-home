from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView

from .models import Settings
from .serializers import SettingsSerializer


class SettingsApi(RetrieveUpdateAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = SettingsSerializer

    def get_object(self):
        return Settings.objects.first()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)