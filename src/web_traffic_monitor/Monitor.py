import database_connections.sql_support_functions as ssf
import pandas as pd

import kabbes_client

import web_traffic_monitor
from web_traffic_monitor import Tables, Base, Slugs
from flask import redirect

class Monitor( Base, kabbes_client.Client ):

    DEFAULT_ATT_VALUES = {
    }

    _OVERRIDE_OPTIONS = {
    1: [ 'Open Slugs', 'run_Child_user' ],
    2: [ 'Query Database', 'query_db_user'],
    5: [ 'test', 'test'],
    6: [ 'Reload', '_import']
    }

    _CONFIG = {
        "_Dir": web_traffic_monitor._Dir
    }

    def __init__( self, *args, **kwargs ):

        Base.__init__( self )
        kabbes_client.Client.__init__( self, *args, **kwargs )

        self.init_db()
        self._import()
        self._Children = [ self.Slugs ]

    def init_db( self ):

        self.db_conn = ssf.get_DatabaseConnection()
        self.db_conn.set_atts( self.cfg.db_conn_kwargs.get_dict()  )
        self.db_conn.get_conn( **self.cfg.db_get_conn_kwargs.get_dict() )
        self.db_conn.get_cursor()

        # initialize tables if they somehow got deleted
        db_tables = self.db_conn.get_all_tables()
        for table in Tables.tables:
            if table not in db_tables:
                df = pd.DataFrame( columns = Tables.tables[table]['columns'] )
                self.db_conn.write( df, table )

    def query_db( self, string: str ) -> pd.DataFrame:
        return self.db_conn.query( string )

    def query_db_user( self ):
        print ( self.query_db( input('Enter your query: ') ) )

    def exit( self ):
        self._export()

    def _import( self ):

        self.Slugs = Slugs.make( self ) # reinitialize the slugs so they start from scratch
        self.Slugs._import()

    def _export( self ):
        self.Slugs._export()

    def run_RTI_choice(self, Slugs_inst):
        Slugs_inst.run()

