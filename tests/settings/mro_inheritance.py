from configurations import Configuration


class GrandParent(Configuration):
    MY_SETTING = 'grandparent'


class Parent1(GrandParent):
    """Does not override MY_SETTING."""
    pass


class Parent2(GrandParent):
    MY_SETTING = 'parent2'


class Child(Parent1, Parent2):
    """
    MRO: Child → Parent1 → Parent2 → GrandParent → Configuration.

    Parent1 does not define MY_SETTING in its own class body, so MRO should
    continue to Parent2, giving MY_SETTING = 'parent2'.
    """
    pass
