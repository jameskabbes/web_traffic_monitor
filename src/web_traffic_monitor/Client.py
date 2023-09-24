import datetime
import importlib

class Client:

    def __init__( self, *engine_args, engine='sqlite3', schema='test', **engine_kwargs ):

        self.schema = getattr( importlib.import_module( '.'+schema, package='web_traffic_monitor.schemas' ) , 'Schema' )
        self.db =     getattr( importlib.import_module( '.'+engine, package='web_traffic_monitor.engines' ) , 'DB' )( self.schema, *engine_args, **engine_kwargs )

    def log_visit( self, slug: str, dt: datetime.datetime = datetime.datetime.utcnow() ):
        
        """log a visit for given slug, defaults to current time, make sure DT has timezone info stored"""

        string = self.schema.log_visit_query( slug, dt )
        self.db.execute_and_commit( string )

    def get_active_redirect( self, slug: str ):

        """get the active redirect of the given slug, returns None if none are active"""

        string = self.schema.get_active_redirect_query( slug )
        result = self.db.query( string )
        if len(result) == 0:
            return None
        return result[0][0]

    def add_redirect( self, slug, redirect, dt: datetime.datetime = datetime.datetime.utcnow() ):

        """deactivates any active redirect for given slug, and adds a new redirect, defaults to current time"""

        self.deactive_redirect( slug, dt )
        string = self.schema.add_redirect_query( slug, redirect, dt )
        self.db.execute_and_commit( string )

    def deactive_redirect( self, slug, dt: datetime.datetime = datetime.datetime.utcnow() ):
        
        """deactivates any active redirect for given slug, defaults END_DATETIME to be current time"""

        string = self.schema.deactivate_redirect_query( slug, dt )
        self.db.execute_and_commit( string )

    