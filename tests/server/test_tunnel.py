import unittest
from localtunnel.server.tunnel import Tunnel


class TestTunnel(unittest.TestCase):
    def test_get_by_hostname(self):
        Tunnel.domain_suffix = 'bar'
        tunnel = Tunnel.create(dict(name='foo', client='Test-Client'))
        self.assertTrue(Tunnel.get_by_hostname('foo.bar'))
        self.assertTrue(Tunnel.get_by_hostname('xxx.foo.bar'))
        self.assertFalse(Tunnel.get_by_hostname('foo.bar.bar'))
        tunnel.destroy()

        Tunnel.domain_suffix = 'foo.bar'
        tunnel = Tunnel.create(dict(name='hello', client='Test-Client'))
        self.assertTrue(Tunnel.get_by_hostname('hello.foo.bar'))
        self.assertTrue(Tunnel.get_by_hostname('world.hello.foo.bar'))
        self.assertFalse(Tunnel.get_by_hostname('foo.bar'))
        self.assertFalse(Tunnel.get_by_hostname('bar'))
        self.assertFalse(Tunnel.get_by_hostname('hello.world.foo.bar'))
        tunnel.destroy()

        Tunnel.domain_suffix = None

    def test_tunnel_callbacks(self):
        Tunnel.domain_suffix = 'bar'
        self.create_called = False
        self.destroy_called = False

        def create_callback(tunnel):
            self.assertEquals(tunnel.name, "foo")
            self.create_called = True

        def destroy_callback(tunnel):
            self.assertEquals(tunnel.name, "foo")
            self.destroy_called = True

        Tunnel.create_callback = create_callback
        Tunnel.destroy_callback = destroy_callback

        tunnel = Tunnel.create(dict(name='foo', client='Test-Client'))
        tunnel.destroy()

        self.assertTrue(self.create_called)
        self.assertTrue(self.destroy_called)
