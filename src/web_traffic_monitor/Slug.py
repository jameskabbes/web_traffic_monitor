from parent_class import ParentClass
from web_traffic_monitor import Columns, Tables, Base, Redirects, Visits, Visit, utils


class Slug( Base ):

    OVERRIDE_OPTIONS = {
    1: [ 'Open Redirects', 'open_Redirects' ],
    2: [ 'Open Visits', 'open_Visits'],
    3: [ 'Log Visit', 'log_Visit']
    }

    def __init__( self, Slugs_inst, slug ):
        Base.__init__( self )

        self.set_attr( Columns.slug, slug ) 
        self.Slugs = Slugs_inst
        self.Redirects = Redirects.make( self )
        self.Visits = Visits.make( self )

    def __len__( self ):
        return 2

    def __iter__( self ):
        self.i = -1
        return self

    def __next__( self ):
        self.i += 1
        if self.i == 0:
            return self.Redirects
        elif self.i == 1:
            return self.Visits
        raise StopIteration
        
    def print_imp_atts(self, **kwargs):
        return self._print_imp_atts_helper( atts = [Columns.slug, 'Redirects','Visits'], **kwargs )

    def print_one_line_atts(self, **kwargs):
        return self._print_one_line_atts_helper( atts = ['type', Columns.slug], **kwargs )

    def display(self):

        return self.get_attr( Columns.slug ) + ', Redirects: ' + str(len(self.Redirects)) + ', Visits: ' + str(len(self.Visits))

    @staticmethod
    def make( *args, **kwargs ):
        return Slug( *args, **kwargs )

    def open_Redirects( self ):
        self.Redirects.run()

    def open_Visits( self ):
        self.Visits.run()

    def delete( self ):
        self.Slugs._remove( self.slug )

    def log_Visit( self ):

        kwargs = {
            Columns.slug: self.slug,
            Columns.datetime: utils.get_current_timestamp()
        }

        new_Visit = self.Visits.make_Visit( **kwargs )
        return new_Visit
