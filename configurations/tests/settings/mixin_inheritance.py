from configurations import Settings


class Mixin1(object):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Mixin1, self).TEMPLATE_CONTEXT_PROCESSORS + (
            'some_app.context_processors.processor1',)


class Mixin2(object):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Mixin2, self).TEMPLATE_CONTEXT_PROCESSORS + (
            'some_app.context_processors.processor2',)


class Inheritance(Mixin2, Mixin1, Settings):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return super(Inheritance, self).TEMPLATE_CONTEXT_PROCESSORS + (
            'some_app.context_processors.processorbase',)
