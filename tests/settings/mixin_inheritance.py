from configurations import Configuration


class Mixin1:
    @property
    def ALLOWED_HOSTS(self):
        allowed_hosts = super().ALLOWED_HOSTS[:]
        allowed_hosts.append('test1')
        return allowed_hosts


class Mixin2:

    @property
    def ALLOWED_HOSTS(self):
        allowed_hosts = super().ALLOWED_HOSTS[:]
        allowed_hosts.append('test2')
        return allowed_hosts


class Inheritance(Mixin2, Mixin1, Configuration):

    def ALLOWED_HOSTS(self):
        allowed_hosts = super().ALLOWED_HOSTS[:]
        allowed_hosts.append('test3')
        return allowed_hosts
