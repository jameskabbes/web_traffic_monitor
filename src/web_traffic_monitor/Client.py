import datetime
import importlib

class Client:

    def __init__( self, *engine_args, engine='sqlite3', schema='test', **engine_kwargs ):

        self.schema = getattr( importlib.import_module( '.'+schema, package='web_traffic_monitor.schemas' ) , 'Schema' )
        self.db =     getattr( importlib.import_module( '.'+engine, package='web_traffic_monitor.engines' ) , 'DB' )( self.schema, *engine_args, **engine_kwargs )

        self.log_visit( 'slug1' )
        self.log_visit( 'slug2' )

    def log_visit( self, slug: str, dt: datetime.datetime = datetime.datetime.utcnow() ):
        
        """log a visit for given slug, defaults to current time, make sure DT has timezone info stored"""

        string = self.schema.QUERIES['LOG_VISIT'].format( SLUG=slug, DATETIME=dt.strftime( self.schema.DT_FORMAT ) )
        self.db.execute_and_commit( string )

    def get_active_redirect( self, slug: str ):

        """get the active redirect of the given slug"""

        string = self.schema.QUERIES['GET_ACTIVE_REDIRECT'].format( SLUG=slug )
        result = self.db.query( string )
        if len(result) == 0:
            return None
        return result[0][0]

    def add_redirect( self, slug, redirect, dt: datetime.datetime = datetime.datetime.utcnow() ):

        self.deactive_redirect( slug, dt )
        string = self.schema.QUERIES['ADD_REDIRECT'].format( SLUG=slug, REDIRECT=redirect, START_DATETIME=dt.strftime( self.schema.DT_FORMAT ) )
        self.execute_and_commit( string )

    def deactive_redirect( self, slug, dt: datetime.datetime ):
    
        string = self.schema.QUERIES['DEACTIVE_REDIRECT'].format( SLUG=slug, END_DATETIME=dt.strftime( self.schema.DT_FORMAT ) )
        self.execute_and_commit( string )
   