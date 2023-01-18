import web_traffic_monitor
import kabbes_client
import py_starter as ps

class Client( web_traffic_monitor.Monitor ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( web_traffic_monitor._Dir, dict=d )
        self.cfg_wtm = self.Package.cfg

        web_traffic_monitor.Monitor.__init__( self )
