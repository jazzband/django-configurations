from .base import Base


class Inheritance(Base):

    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return tuple(super(Inheritance, self).TEMPLATE_CONTEXT_PROCESSORS) + (
            'tests.settings.base.test_callback',)
