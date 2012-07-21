from .base import Base


class Inheritance(Base):

    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Inheritance, self).TEMPLATE_CONTEXT_PROCESSORS + (
            'configurations.tests.settings.base.test_callback',)
