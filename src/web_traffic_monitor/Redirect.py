from web_traffic_monitor import Columns, Tables, Parent, utils


import py_starter as ps
import pandas as pd

class Redirect( Parent ):

    OVERRIDE_OPTIONS = {
    1: [ 'Make Inactivate', 'terminate' ]
    }

    def __init__( self, Redirects_inst, **kwargs ):
        Parent.__init__( self )
        self.set_atts( kwargs )
        self.Redirects = Redirects_inst

    def __len__( self ):
        return 1
    def __iter__( self ):
        return self
    def __next__( self ):
        return StopIteration
    def __eq__( self, other ):
        try:
            other.get_attr( Columns.redirect ) == self.get_attr( Columns.redirect )
        except:
            return False
        return True

    def print_imp_atts(self, **kwargs):
        return self._print_imp_atts_helper( atts = [Columns.id, Columns.slug, Columns.redirect, Columns.datetime_start, Columns.datetime_end, Columns.is_current],
                                            **kwargs)

    def print_one_line_atts(self, **kwargs):
        return self._print_one_line_atts_helper( atts = ['type', Columns.slug, Columns.redirect, Columns.is_current],
                                                **kwargs )
            
    @staticmethod
    def make( *args, **kwargs ):
        return Redirect( *args, **kwargs )

    @staticmethod
    def make_user( Slugs_inst ):

        while True:
            slug = input('Enter the slug (enter to exit): ')
            if slug == '':
                return None

            if slug not in Slugs_inst.Slugs:
                Slugs_inst.add_Slug( slug )
            else:
                if not ps.confirm_raw( 'This Slug already exists.' ):
                    continue

            if ps.confirm_raw( 'You entered ' + slug ):
                break
        
        Slugs_inst.Slugs[slug].print_atts()
        Slugs_inst.Slugs[slug].Redirects.print_atts()
        print ()

        while True:
            redirect = input('Enter the redirect (enter to exit): ')
            if redirect == '':
                return None

            current_redirects = Slugs_inst.Slugs[slug].Redirects.get_current()

            active = False
            for current_Redirect_inst in current_redirects:
                if current_Redirect_inst.get_attr( Columns.redirect ) == redirect:
                    print ('Redirect already active for this Slug')
                    active = True
                    break
            if active:
                continue
            
            if ps.confirm_raw('You have entered the redirect: ' + redirect):
                break
        
        for current_Redirect_inst in current_redirects:
            current_Redirect_inst.terminate()

        kwargs = {
            Columns.slug: slug,
            Columns.redirect: redirect
        }

        new_Redirect_inst = Redirect.make( Slugs_inst.Slugs[slug].Redirects, **kwargs )   
        new_Redirect_inst.initialize()

        return new_Redirect_inst

    def initialize( self ):
        
        self.get_id()
        self.make_current()
        self.set_attr( Columns.datetime_start, utils.get_current_timestamp() )
        self.set_attr( Columns.datetime_end  , utils.get_max_timestamp() )

    def get_id( self ):

        self.set_attr( Columns.id, utils.get_nanoid() )

    def terminate( self ):

        self.make_past()
        self.set_attr( Columns.datetime_end , utils.get_current_timestamp() )

    def make_current( self ):
        self.set_attr( Columns.is_current , True )

    def make_past( self ):
        self.set_attr( Columns.is_current , False )

    def string_found_in_Children( self, string_lower ):
        
        for column in Columns.searchable:
            if string_lower in self.get_attr( column ):
                return [ self ]
        return []

    def delete( self ):
        self.Redirects._remove( self )

    def export( self ) -> pd.DataFrame:
        return utils.turn_class_atts_into_df_row( self, Tables.tables[ Tables.dim ]['columns'] )
