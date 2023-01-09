import web_traffic_monitor
import kabbes_user_client
import py_starter as ps

class Client( web_traffic_monitor.Monitor ):

    BASE_CONFIG_DICT = {
        "_Dir": web_traffic_monitor._Dir
    }

    def __init__( self, dict={}, **kwargs ):

        dict = ps.merge_dicts( Client.BASE_CONFIG_DICT, dict )
        self.cfg_wtm = kabbes_user_client.Client( dict=dict, **kwargs ).cfg
        web_traffic_monitor.Monitor.__init__( self )
