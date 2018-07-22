from django.template.loaders.filesystem import Loader

from .base import ConditionalJinja2LoaderMixin


class MyLoader(ConditionalJinja2LoaderMixin, Loader):

    def __init__(self, engine, dirs=None):
        super().__init__(engine)
        self.dirs = dirs

    pass

_loader = MyLoader()
