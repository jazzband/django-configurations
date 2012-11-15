
from configurations import Settings


class BaseSettings(Settings):
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(BaseSettings, self).TEMPLATE_CONTEXT_PROCESSORS


class Klass1(BaseSettings):
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Klass1, self).TEMPLATE_CONTEXT_PROCESSORS() + (
            'configurations.tests.settings.base.test_callback1',)


class Klass2(BaseSettings):
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Klass2, self).TEMPLATE_CONTEXT_PROCESSORS() + (
            'configurations.tests.settings.base.test_callback2',)


class Klass3(BaseSettings):
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Klass3, self).TEMPLATE_CONTEXT_PROCESSORS() + (
            'configurations.tests.settings.base.test_callback3',)


class MInheritance(Klass1, Klass2, Klass3):
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(MInheritance, self).TEMPLATE_CONTEXT_PROCESSORS() + (
            'configurations.tests.settings.base.test_callback_m',)
