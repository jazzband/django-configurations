from configurations import Configuration, environ_prefix, values


@environ_prefix("ACME")
class PrefixDecoratorConf1(Configuration):
    FOO = values.Value()


@environ_prefix("ACME")
class PrefixDecoratorConf2(Configuration):
    FOO = values.BooleanValue(False)


@environ_prefix("ACME")
class PrefixDecoratorConf3(Configuration):
    FOO = values.Value(environ_prefix="ZEUS")


@environ_prefix("")
class PrefixDecoratorConf4(Configuration):
    FOO = values.Value()


@environ_prefix(None)
class PrefixDecoratorConf5(Configuration):
    FOO = values.Value()
