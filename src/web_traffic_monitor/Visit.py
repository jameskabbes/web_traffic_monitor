from web_traffic_monitor import Tables, Columns, Base, utils
import kabbes_menu

import py_starter as ps
import pandas as pd

class Visit( Base, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {}

    _IMP_ATTS = [Columns.slug, Columns.datetime]
    _ONE_LINE_ATTS = ['type', Columns.datetime, Columns.slug]
    _SEARCHABLE_ATTS = [ Columns.datetime ]

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self, Visits_inst, **kwargs ):
        Base.__init__( self )
        kabbes_menu.Menu.__init__( self )
        self.set_atts( kwargs )
        self.Visits = Visits_inst

    @staticmethod
    def make( *args, **kwargs ):
        return Visit( *args, **kwargs )

    @staticmethod
    def make_user( Slugs_inst ):

        while True:
            slug = input('Enter the slug (enter to exit): ')
            if slug == '':
                return None

            if slug not in Slugs_inst.Slugs:
                Slugs_inst.make_Slug( slug )
            else:
                if not ps.confirm_raw( 'This Slug already exists.' ):
                    continue

            if ps.confirm_raw( 'You entered ' + slug ):
                break
        
        Slugs_inst.Slugs[slug].print_atts()
        Slugs_inst.Slugs[slug].Visits.print_atts()

        kwargs = {
            Columns.slug: slug,
            Columns.datetime: utils.get_current_timestamp()
        }

        new_Visit_inst = Visit.make( Slugs_inst.Slugs[slug].Visits, **kwargs )
        return new_Visit_inst


    def delete( self ):
        self.Visits._remove( self )

    def export( self ) -> pd.DataFrame:
        return utils.turn_class_atts_into_df_row( self, Tables.tables[ Tables.visits ]['columns'] )
