from .single_inheritance import Inheritance as BaseInheritance


class Inheritance(BaseInheritance):

    def ALLOWED_HOSTS(self):
        allowed_hosts = super(Inheritance, self).ALLOWED_HOSTS[:]
        allowed_hosts.append('test-test')
        return allowed_hosts
