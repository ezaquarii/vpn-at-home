from vpnathome.tests import APITestWithBaseFixture

from ..models import BlockListUrl
from ..serializers import BlockListUrlSerializer, BlockListUrlUpdateSerializer


class TestBlockListUrlSerializer(APITestWithBaseFixture):

    def setUp(self):
        self.urls = BlockListUrl.objects.all()
        self.assertTrue(len(self.urls) > 0, "Some URLs should be added by default during DB migration")

    def test_serializer(self):
        serializer = BlockListUrlSerializer(self.urls, many=True)
        self.assertEquals(len(serializer.data), len(self.urls))


class TestBlockListUrlUpdateSerializer(APITestWithBaseFixture):

    def setUp(self):
        self.urls = BlockListUrl.objects.all()
        self.data = BlockListUrlSerializer(self.urls, many=True).data

    def test_validates_proper_data(self):
        serializer = BlockListUrlUpdateSerializer(data=self.data, many=True)
        serializer.is_valid(raise_exception=True)

    def test_required_id(self):
        self.data[-1].pop('id')
        serializer = BlockListUrlUpdateSerializer(data=self.data, many=True, require_id=True)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('id' in serializer.errors[-1])

    def test_update_with_required_id_is_not_possible(self):
        instance = self.urls[0]
        update_data = BlockListUrlUpdateSerializer(instance).data
        update_serializer = BlockListUrlUpdateSerializer(instance=instance, data=update_data, partial=True, require_id=True)
        update_serializer.is_valid(raise_exception=True)
        with self.assertRaises(RuntimeError):
            update_serializer.save()
