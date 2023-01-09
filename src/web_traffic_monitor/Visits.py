from parent_class import ParentPluralList
from web_traffic_monitor import Base, Visit
import kabbes_menu

import py_starter as ps
import pandas as pd

class Visits( ParentPluralList, Base, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Visit', 'run_Child_user' ],
    "7": [ '', 'do_nothing' ]
    }

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self, Slug_inst ):
        ParentPluralList.__init__( self, 'Visits' )
        Base.__init__( self )
        kabbes_menu.Menu.__init__( self )

        self.Slug = Slug_inst

    @staticmethod
    def make( *args, **kwargs ):
        return Visits( *args, **kwargs )

    def make_Visit( self, **kwargs ):
        new_Visit = Visit.make( self, **kwargs )
        self.add_Visit( new_Visit ) 
        return new_Visit

    def add_Visit( self, Visit_inst ):
        self._add( Visit_inst )

    def export( self ) -> pd.DataFrame:

        dfs = [ Visit_inst.export() for Visit_inst in self ]
        return pd.concat( dfs )

