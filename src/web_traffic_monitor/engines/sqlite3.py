from web_traffic_monitor.engines.base import DB as BaseDB
import sqlite3

class DB( BaseDB ):

    GET_TABLES_QUERY = 'SELECT name FROM sqlite_master WHERE type="table";'

    def __init__( self, schema, *args, path='web_traffic_monitor.db', **kwargs ):
        self.conn = sqlite3.connect( path )
        BaseDB.__init__( self, schema )

    def query( self, string: str ):
        print (string)
        return self.conn.execute( string ).fetchall()

    def execute( self, string: str ):
        print (string)
        self.conn.execute( string )

    def commit( self ):
        self.conn.commit()

