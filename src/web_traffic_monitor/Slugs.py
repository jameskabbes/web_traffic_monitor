from parent_class import ParentPluralDict
from web_traffic_monitor import Columns, Tables, Parent, Redirect, Visit, Slug, utils
import pandas as pd

import py_starter as ps

class Slugs( Parent, ParentPluralDict ):

    OVERRIDE_OPTIONS = {
    1: [ 'Open Slug', 'open_Child_user' ],
    2: [ 'Make New Redirect', 'make_Redirect_user'],
    3: [ 'Make New Visit', 'make_Visit_user'],
    7: [ '', 'do_nothing' ]
    }  

    def __init__( self, Editor_inst, **kwargs ):
        ParentPluralDict.__init__( self, 'Slugs' )
        Parent.__init__( self )
        self.Editor = Editor_inst

    @staticmethod
    def make( *args, **kwargs ):
        return Slugs( *args, **kwargs )

    def add_Slug( self, slug ):

        new_Slug = Slug.make( self, slug )
        self._add( slug, new_Slug )
    
    def make_Visit( self, **kwargs ):
        
        slug = kwargs[ Columns.slug ]
        if slug not in self.Slugs:
            self.add_Slug( slug )

        new_Visit = Visit.make( self.Slugs[ slug ].Visits, **kwargs )
        self._add_Visit( new_Visit )        

    def _add_Visit( self, Visit_inst ):

        slug = Visit_inst.get_attr( Columns.slug )
        if slug not in self.Slugs:
            self.add_Slug( slug )

        self.Slugs[ slug ].Visits.add_Visit( Visit_inst )

    def make_Redirect_user( self ):

        new_Redirect = Redirect.make_user( self )
        if new_Redirect != None:
            self._add_Redirect( new_Redirect )

    def make_Redirect( self, **kwargs ):

        slug = kwargs[ Columns.slug ]
        if slug not in self.Slugs:
            self.add_Slug( slug )
        
        new_Redirect = Redirect.make( self.Slugs[ slug ].Redirects, **kwargs )
        self._add_Redirect( new_Redirect )

    def _add_Redirect( self, Redirect_inst ):
        self.Slugs[ Redirect_inst.get_attr(Columns.slug) ].Redirects.add_Redirect( Redirect_inst )

    def make_Visit_user( self ):

        new_Visit = Visit.make_user( self )
        if new_Visit != None:
            self._add_Visit( new_Visit )

    def make_Visit( self, **kwargs ):

        slug = kwargs[ Columns.slug ]
        if slug not in self.Slugs:
            self.add_Slug( slug )
        
        new_Visit = Visit.make( self.Slugs[ slug ].Visits, **kwargs )
        self._add_Visit( new_Visit )

    def _add_Visit( self, Visit_inst ):
        self.Slugs[ Visit_inst.get_attr(Columns.slug) ].Visits.add_Visit( Visit_inst )

    def _import( self ):

        df_redirects = self.Editor.db_conn.query( 'Select * from ' + Tables.redirects )
        df_redirects = utils.prep_df_for_import( df_redirects )

        for i in range(len(df_redirects)):
            kwargs = utils.turn_df_row_into_kwargs( df_redirects.loc[i], Tables.tables[ Tables.redirects ]['columns'] )
            self.make_Redirect( **kwargs )

        df_visits = self.Editor.db_conn.query( 'Select * from visits' )
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

        self.Editor.db_conn.write( df_redirects, Tables.redirects, if_exists='replace' )
        self.Editor.db_conn.write( df_visits, Tables.visits, if_exists='replace' )

    def run_RTI_choice(self, Slug_inst):

        Slug_inst.run()
