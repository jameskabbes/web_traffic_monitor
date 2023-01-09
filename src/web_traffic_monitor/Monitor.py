import database_connections.sql_support_functions as ssf
import pandas as pd

import kabbes_menu

import web_traffic_monitor
from flask import redirect

class Monitor( web_traffic_monitor.Base, kabbes_menu.Menu ):

    DEFAULT_ATT_VALUES = {
    }

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Slugs', 'run_Child_user' ],
    "2": [ 'Query Database', 'query_db_user'],
    "6": [ 'Reload', '_import'],
    "7": [ "Print Config", "print_config"]
    }

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self ):

        web_traffic_monitor.Base.__init__( self )   
        kabbes_menu.Menu.__init__( self )

        self.init_db()
        self._import()
        self._Children = [ self.Slugs ]

    def print_config( self ):

        self.cfg_wtm.print_atts()

    def init_db( self ):

        self.db_conn = ssf.get_DatabaseConnection()
        self.db_conn.set_atts( self.cfg_wtm['db_conn_kwargs'].get_dict()  )
        self.db_conn.get_conn( **self.cfg_wtm['db_get_conn_kwargs'].get_dict() )
        self.db_conn.get_cursor()

        # initialize tables if they somehow got deleted
        db_tables = self.db_conn.get_all_tables()
        for table in web_traffic_monitor.Tables.tables:
            if table not in db_tables:
                df = pd.DataFrame( columns = web_traffic_monitor.Tables.tables[table]['columns'] )
                self.db_conn.write( df, table )

    def query_db( self, string: str ) -> pd.DataFrame:
        return self.db_conn.query( string )

    def query_db_user( self ):
        print ( self.query_db( input('Enter your query: ') ) )

    def exit( self ):
        self._export()

    def _import( self ):

        self.Slugs = web_traffic_monitor.Slugs.make( self ) # reinitialize the slugs so they start from scratch
        self.Slugs._import()

    def _export( self ):
        self.Slugs._export()

    def run_RTI_choice(self, Slugs_inst):
        Slugs_inst.run()

