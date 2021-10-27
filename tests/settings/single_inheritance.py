from .base import Base


class Inheritance(Base):

    @property
    def ALLOWED_HOSTS(self):
        allowed_hosts = super().ALLOWED_HOSTS[:]
        allowed_hosts.append('test')
        return allowed_hosts
