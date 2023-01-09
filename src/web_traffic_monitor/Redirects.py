from parent_class import ParentPluralList 

from web_traffic_monitor import Columns, Tables, utils, Base, Redirect
import kabbes_menu
import py_starter as ps
import pandas as pd

class Redirects( ParentPluralList, Base, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Redirect', 'run_Child_user' ],
    "7": [ '', 'do_nothing' ]
    }

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self, Slug_inst ):
        ParentPluralList.__init__( self, 'Redirects' )
        Base.__init__( self )
        kabbes_menu.Menu.__init__( self )
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

