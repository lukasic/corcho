from django.apps import AppConfig


class ChoosingConfig(AppConfig):
    name = 'app.choosing'

    def ready(self):
        __import__('{}.signals'.format(self.name))
