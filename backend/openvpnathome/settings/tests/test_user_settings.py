import tempfile
from os import path
from unittest import TestCase
import uuid

from openvpnathome.settings import UserSettings, DEFAULT_USER_SETTINGS


class TestDefaultUserSettings(TestCase):

    def test_loads_default_settings(self):
        settings = UserSettings(settings_file_path='/some-non-existing-file')
        self.assertEqual(settings.email_enabled, DEFAULT_USER_SETTINGS['email']['enabled'])


class TestWriteUserSettings(TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.settings_file_path = path.join(self.tmp_dir, 'settings.json')
        self.assertFalse(path.exists(self.settings_file_path))
        self.settings = DEFAULT_USER_SETTINGS.copy()
        self.secret_key = str(uuid.uuid4())
        self.settings['secret_key'] = self.secret_key

    def test_write_settings(self):
        s = UserSettings(settings_file_path=self.settings_file_path, settings=self.settings)
        s.write()
        self.assertTrue(path.isfile(self.settings_file_path))

    def test_write_read_settings(self):
        writer = UserSettings(settings_file_path=self.settings_file_path, settings=self.settings)
        writer.write()

        reader = UserSettings(settings_file_path=self.settings_file_path)
        self.assertEqual(reader.secret_key, self.secret_key)
