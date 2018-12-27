from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from django.views import View

from vpnathome.utils import filter_objects_to_map_by_pk
from .models import Settings, BlockListUrl
from .serializers import SettingsSerializer, BlockListUrlSerializer, BlockListUrlUpdateSerializer


class SettingsApi(RetrieveUpdateAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = SettingsSerializer

    def get_object(self):
        return Settings.objects.first()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlockListUrlApi(ViewSet):

    permission_classes = [IsAdminUser]

    def list(self, request):
        urls = BlockListUrl.objects.all()
        serializer = BlockListUrlSerializer(urls, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        validator = BlockListUrlUpdateSerializer(data=request.data, many=True, require_id=True)
        validator.is_valid(raise_exception=True)
        updates = {item['id']: item for item in validator.data}
        items = {item.id: item for item in BlockListUrl.objects.filter(id__in=updates.keys())}
        for update_id, update_item in updates.items():
            update_serializer = BlockListUrlUpdateSerializer(items[update_id], data=update_item)
            update_serializer.is_valid(raise_exception=True)
            update_serializer.save()
        return Response(status=status.HTTP_200_OK)


class Test500Error(View):

    def get(self, request):
        raise RuntimeError('Test error e-mail')
