from flask import Flask, redirect, abort
from web_traffic_monitor import Client, queries, Columns, Tables
import functools
import py_starter as ps

class FlaskMonitor( Flask, Client ):

    def __init__( self, *Flask_args, Client_kwargs = {}, **Flask_kwargs ):
        Client.__init__( self, dict=Client_kwargs )
        Flask.__init__( self, *Flask_args, **Flask_kwargs )

    def wtm_route( self, slug_formatted ):
        def decorator( func ):
            
            @self.route( slug_formatted ) #traditional Flask app.route()
            @functools.wraps( func )
            def wrapper( *called_args, **called_kwargs ): #flask unpacks the slug string and passes it into kwargs

                slug_raw_path = ps.smart_format( slug_formatted, called_kwargs, trigger_beg='<',trigger_end='>' )
                
                print (slug_formatted)
                print (slug_raw_path)

                self.log_Visit( slug_raw_path[1:] ) #remove the '/' 
                return func( *called_args, **called_kwargs )

            return wrapper
        return decorator
    
    def wtm_redirect( self, slug ):

        url = self.get_active_Redirect( slug )

        if url != None:
            return redirect( url )
        else:
            abort(404)

    def log_Visit(self, slug):

        """add a row to the Visits table"""

        new_Visit = self.Slugs.log_Visit( slug )
        df_Visit = new_Visit.export()
        self.db_conn.write( df_Visit, Tables.visits, if_exists='append' )

    def get_active_Redirect( self, slug ) -> str:

        """returns the redirect url for the given slug"""

        df_redirects = self.query_db( queries.get_active_redirect( slug ) )

        if len(df_redirects) > 0:
            return df_redirects.loc[ 0, Columns.redirect ]
        else:
            abort(404)
