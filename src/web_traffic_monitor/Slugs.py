from parent_class import ParentPluralDict
from web_traffic_monitor import Columns, Tables, Base, Redirect, Visit, Slug, utils
import pandas as pd

import py_starter as ps

class Slugs( Base, ParentPluralDict ):

    OVERRIDE_OPTIONS = {
    1: [ 'Open Slug', 'open_Child_user' ],
    2: [ 'Make New Redirect', 'make_Redirect_user'],
    3: [ 'Make New Visit', 'make_Visit_user'],
    7: [ '', 'do_nothing' ]
    }  

    def __init__( self, Monitor_inst, **kwargs ):
        ParentPluralDict.__init__( self, 'Slugs' )
        Base.__init__( self )
        self.Monitor = Monitor_inst

    @staticmethod
    def make( *args, **kwargs ):
        return Slugs( *args, **kwargs )

    def make_Slug( self, slug ):
        new_Slug = Slug.make( self, slug )
        self.add_Slug( new_Slug )
        return new_Slug

    def add_Slug( self, Slug_inst ):
        self._add( Slug_inst.get_attr( Columns.slug ), Slug_inst )

    def check_and_make_Slug( self, slug ):
        if slug not in self.Slugs:
            self.make_Slug( slug )
    
    ### Visit
    def make_Visit( self, **kwargs ):
        
        """Make and add visit"""

        slug = kwargs[ Columns.slug ]
        self.check_and_make_Slug( slug )
        
        new_Visit = self.Slugs[ slug ].Visits.make_Visit( **kwargs )

    def log_Visit( self, slug ):

        self.check_and_make_Slug( slug )
        return self.Slugs[ slug ].log_Visit()

    def make_Visit_user( self ):

        new_Visit = Visit.make_user( self )
        if new_Visit != None:
            self._add_Visit( new_Visit )

    ### Redirect
    def make_Redirect_user( self ):

        new_Redirect = Redirect.make_user( self )
        if new_Redirect != None:
            self._add_Redirect( new_Redirect )

    def make_Redirect( self, **kwargs ):

        slug = kwargs[ Columns.slug ]
        self.check_and_make_Slug( slug )
        
        new_Redirect = Redirect.make( self.Slugs[ slug ].Redirects, **kwargs )
        self._add_Redirect( new_Redirect )

    def _add_Redirect( self, Redirect_inst ):
        self.Slugs[ Redirect_inst.get_attr(Columns.slug) ].Redirects.add_Redirect( Redirect_inst )

    ### IO
    def _import( self ):

        df_redirects = self.Monitor.db_conn.query( 'Select * from ' + Tables.redirects )
        df_redirects = utils.prep_df_for_import( df_redirects )

        for i in range(len(df_redirects)):
            kwargs = utils.turn_df_row_into_kwargs( df_redirects.loc[i], Tables.tables[ Tables.redirects ]['columns'] )
            self.make_Redirect( **kwargs )

        df_visits = self.Monitor.db_conn.query( 'Select * from visits' )
        df_visits = utils.prep_df_for_import( df_visits )

        for i in range(len(df_visits)):
            kwargs = utils.turn_df_row_into_kwargs( df_visits.loc[i], Tables.tables[ Tables.visits ]['columns'])
            self.make_Visit( **kwargs )

    def _export( self ):

        # redirects
        df_redirects = pd.DataFrame( columns = Tables.tables[Tables.redirects]['columns'] )
        df_visits = pd.DataFrame( columns = Tables.tables[Tables.visits]['columns'] )

        for Slug_inst in self:
            
            for Redirect_inst in Slug_inst.Redirects:
                df_redirects_row = utils.turn_class_atts_into_df_row( Redirect_inst, Tables.tables[ Tables.redirects ]['columns'] )
                df_redirects = df_redirects.append( df_redirects_row )      

            for Visit_inst in Slug_inst.Visits:
                df_visits_row = utils.turn_class_atts_into_df_row( Visit_inst, Tables.tables[ Tables.visits ]['columns'] )
                df_visits = df_visits.append( df_visits_row )      

        df_redirects.reset_index(drop=True, inplace=True)
        df_visits.reset_index(drop=True, inplace=True)

        df_redirects =    utils.prep_df_for_export( df_redirects )
        df_visits = utils.prep_df_for_export( df_visits )

        self.Monitor.db_conn.write( df_redirects, Tables.redirects, if_exists='replace' )
        self.Monitor.db_conn.write( df_visits, Tables.visits, if_exists='replace' )

    def run_RTI_choice(self, Slug_inst):

        Slug_inst.run()
