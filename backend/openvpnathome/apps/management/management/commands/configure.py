from os import path
from random import SystemRandom

from django.contrib.auth import get_user_model
from django.template import engines

from . import ManagementCommand

import openvpnathome
from openvpnathome.utils import get_object_or_none

CONFIG_DIR = path.dirname(openvpnathome.__file__)
CONFIG_TEMPLATE_FILE_PATH = path.join(CONFIG_DIR, 'config.py.example')
CONFIG_FILE_PATH = path.join(CONFIG_DIR, 'config.py')

User = get_user_model()


class Command(ManagementCommand):

    # important, as db is not available before generating config;
    # don't run command under db transaction
    uses_db = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('-d', '--development', action='store_true', help="Configure for development")
        parser.add_argument('-p', '--preview', action='store_true', help="Dump generated config to stdout, do not write.")
        parser.add_argument('-c', '--config-template', help='Supply your own configuration file template.')
        parser.add_argument('-f', '--force', action='store_true', help="Force overwriting config if it already exists")

    @property
    def option_development(self):
        return self.options.get('development', False)

    @property
    def option_no_warnings(self):
        return self.options.get('development', False)

    @property
    def option_config_template(self):
        template = self.options.get('config_template')
        return template if template is not None else CONFIG_TEMPLATE_FILE_PATH

    @property
    def option_preview(self):
        return self.options.get('preview', False)

    @property
    def option_force(self):
        return self.options.get('force', False)

    def run(self, *args, **options):
        if path.exists(CONFIG_FILE_PATH) and not self.option_preview and not self.option_force:
            self.warn('Config file already exist. Skipping.')
        else:
            if not path.isfile(self.option_config_template):
                raise FileNotFoundError('Config template {} not found'.format(self.option_config_template))
            with open(self.option_config_template, "r") as config_template_file:
                config_template = config_template_file.read()

            engine = engines['django']
            template = engine.from_string(config_template)
            config = template.render(context=self.config_context)

            if self.option_preview:
                print(config)
            else:
                with open(CONFIG_FILE_PATH, 'w') as config_file:
                    config_file.write(config)

            if self.option_development:
                self.log('Created configuration file to {file} (development)'.format(file=CONFIG_FILE_PATH))
            else:
                self.log('Created configuration file to {file}'.format(file=CONFIG_FILE_PATH))

    @property
    def config_context(self):
        admin = get_object_or_none(User, is_superuser=True)
        return {
            'email_to_admin': admin.email if admin else '',
            'development': self.option_development,
            'secret_key': self.create_secret_key()
        }

    def create_secret_key(self):
        return ''.join([SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
