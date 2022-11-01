from parent_class import ParentPluralList
from web_traffic_monitor import Base, Visit

import py_starter as ps
import pandas as pd

class Visits( Base, ParentPluralList ):

    OVERRIDE_OPTIONS = {
    1: [ 'Open Visit', 'open_Child_user' ],
    7: [ '', 'do_nothing' ]
    }


    def __init__( self, Slug_inst ):
        ParentPluralList.__init__( self, 'Visits' )
        Base.__init__( self )
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

