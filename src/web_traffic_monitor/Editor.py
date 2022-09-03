import database_connections.sql_support_functions as ssf
import pandas as pd

from web_traffic_monitor import Tables, Parent, Slugs

class Editor( Parent ):

    DEFAULT_ATT_VALUES = {
        'db_conn_kwargs' : {
            'db_path': './Data/urls.db',
            'connection_module': 'sqlite'
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
        Parent.__init__( self, **kwargs )
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

        self.db_conn = ssf.get_DatabaseConnection( **self.db_conn_kwargs )

        # initialize tables if they somehow got deleted
        db_tables = self.db_conn.get_all_tables()
        for table in Tables.tables:
            if table not in db_tables:
                df = pd.DataFrame( columns = Tables.tables[table]['columns'] )
                self.db_conn.write( df, table )


    def query_db( self ):
        print ( self.db_conn.query( input('Enter your query: ') ) )

    def exit( self ):
        self._export()

    def _import( self ):

        self.Slugs = Slugs.make( self )
        self.Slugs._import()

    def _export( self ):

        self.Slugs._export()

    def test( self ):
        pass

    def run_RTI_choice(self, Slugs_inst):

        Slugs_inst.run()

