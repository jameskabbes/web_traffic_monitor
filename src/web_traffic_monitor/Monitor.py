import database_connections.sql_support_functions as ssf
import pandas as pd

from web_traffic_monitor import Tables, Base, Slugs
from flask import redirect

class Monitor( Base ):

    DEFAULT_ATT_VALUES = {
        'db_conn_kwargs' : {
            'db_path': './Data/web_traffic_monitor.db',
            'connection_module': 'sqlite'
        },
        'db_get_conn_kwargs': {
            'check_same_thread': False
        }
    }

    OVERRIDE_OPTIONS = {
    1: [ 'Open Slugs', 'open_Child_user' ],
    2: [ 'Query Database', 'query_db'],
    5: [ 'test', 'test'],
    6: [ 'Reload', '_import'],
    7: [ '', 'do_nothing' ]
    }

    def __init__( self, **kwargs ):
        super().__init__(  **kwargs )
        self.init_db()
        self._import()

    def __len__( self ):
        return 1
    def __iter__( self ):
        self.i = -1
        return self
    def __next__( self ):
        self.i += 1
        if self.i == 0:
            return self.Slugs
        raise StopIteration

    def init_db( self ):

        self.db_conn = ssf.get_DatabaseConnection()
        self.db_conn.set_atts( self.db_conn_kwargs  )
        self.db_conn.get_conn( **self.db_get_conn_kwargs )
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

