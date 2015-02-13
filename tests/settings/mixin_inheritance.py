from configurations import Configuration


class Mixin1(object):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return tuple(super(Mixin1, self).TEMPLATE_CONTEXT_PROCESSORS) + (
            'some_app.context_processors.processor1',)


class Mixin2(object):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return tuple(super(Mixin2, self).TEMPLATE_CONTEXT_PROCESSORS) + (
            'some_app.context_processors.processor2',)


class Inheritance(Mixin2, Mixin1, Configuration):

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return tuple(super(Inheritance, self).TEMPLATE_CONTEXT_PROCESSORS) + (
            'some_app.context_processors.processorbase',)
