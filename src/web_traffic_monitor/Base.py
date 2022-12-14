import py_starter as ps
from kabbes_menu import Menu

class Base( Menu ):

    DEFAULT_ATT_VALUES = {}

    def __init__( self, **kwargs ):
        Menu.__init__( self )

        ### Setup kwargs
        kwargs = ps.replace_default_kwargs( self.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

    def delete( self ):

        if ps.confirm_raw( 'This will delete ' + self.print_one_line_atts() ):
            self.delete_self()

    def delete_self( self ):
        pass

