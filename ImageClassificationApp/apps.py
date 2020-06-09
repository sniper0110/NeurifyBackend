from django.apps import AppConfig


class ImageclassificationappConfig(AppConfig):
    name = 'ImageClassificationApp'

    def ready(self):
        import ImageClassificationApp.signals
