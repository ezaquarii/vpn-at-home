from unittest import TestCase

from openvpnathome.utils import get_nested_item
from openvpnathome import utils


class TestGetNestedItem(TestCase):

    obj = {'a': {'b': {'c': 1}}}

    def test_get_existing_item(self):
        item = get_nested_item(self.obj, 'a.b.c')
        self.assertEqual(item, 1)

    def test_get_nonexisting_item_1(self):
        try:
            item = get_nested_item(self.obj, 'a.b.c.d')
            self.fail()
        except KeyError:
            pass

    def test_get_nonexisting_item_2(self):
        try:
            item = get_nested_item(self.obj, 'a.b.x')
            self.fail()
        except KeyError:
            pass


class TestIsDatabaseMigrated(TestCase):

    def test_is_migrated(self):
        self.assertTrue(utils.is_database_migrated())

    def test_unknown_database_is_not_migrated(self):
        self.assertFalse(utils.is_database_migrated('unknown-database'))
