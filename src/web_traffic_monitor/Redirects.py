from parent_class import ParentPluralList 

from web_traffic_monitor import Columns, Tables, utils, Base, Redirect

import py_starter as ps
import pandas as pd

class Redirects( Base, ParentPluralList ):

    OVERRIDE_OPTIONS = {
    1: [ 'Open Redirect', 'open_Child_user' ],
    7: [ '', 'do_nothing' ]
    }

    def __init__( self, Slug_inst ):
        ParentPluralList.__init__( self, 'Redirects' )
        Base.__init__( self )
        self.Slug = Slug_inst

    @staticmethod
    def make( *args, **kwargs ):
        return Redirects( *args, **kwargs )

    def make_Redirect( self, **kwargs ):
        new_Redirect = Redirect.make( self, **kwargs )
        return new_Redirect

    def add_Redirect( self, Redirect_inst ):
        self._add( Redirect_inst )

    def get_current( self ):
        
        for Redirect_inst in self:
            if Redirect_inst.get_attr( Columns.is_current ):
                return Redirect_inst
        return None

    def export( self ) -> pd.DataFrame:

        dfs = [ Redirect_inst.export() for Redirect_inst in self ]
        return pd.concat( dfs )

