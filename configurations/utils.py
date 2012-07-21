def isuppercase(name):
    return name == name.upper() and not name.startswith('_')


def uppercase_attributes(obj):
    return dict((name, getattr(obj, name))
                for name in filter(isuppercase, dir(obj)))
