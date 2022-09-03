from parent_class import ParentClass
from web_traffic_monitor import CustomRTI
import py_starter as ps

class Parent( ParentClass ):

    BASE_OPTIONS = {
    1: ['','do_nothing'],
    2: ['','do_nothing'],
    3: ['','do_nothing'],
    4: ['','do_nothing'],
    5: ['','do_nothing'],
    6: ['','do_nothing'],
    7: ['Delete','delete_user'],
    8: ['Print All Attributes', 'print_all_atts'],
    9: ['Print Important Attributes', 'print_imp_atts'],
    }

    DEFAULT_ATT_VALUES = {}
    OVERRIDE_OPTIONS = {}

    def __init__( self, **kwargs ):

        ParentClass.__init__( self )

        ### Setup kwargs
        kwargs = ps.replace_default_kwargs( self.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

        ### Get Options setup
        self.OPTIONS = self.BASE_OPTIONS.copy()
        self.OPTIONS.update( self.OVERRIDE_OPTIONS )

        self.RTI = CustomRTI( self )

    def __str__( self ):
        return self.display()

    def display( self ):

        return self.print_one_line_atts( print_off = False, leading_string='' )

    def open_Child_user( self ):

        Child_inst = ps.get_selection_from_list( self )
        if Child_inst != None:
            Child_inst.run()

    def do_nothing( self ):
        pass

    def run_RTI_choice( self, choice ):
        pass

    def right_before_run( self ):
        pass

    def string_found_in_Children( self, string ):

        viable_Children = []
        for Child_obj in self:
            if len(Child_obj.string_found_in_Children( string )) > 0:
                viable_Children.append( Child_obj )

        return viable_Children

    @ps.confirm_wrap('Performing delete.')
    def delete_user( self ):
        self.delete()

    def delete( self ):
        pass

    def run( self ):

        self.right_before_run()
        while True:

            self.print_one_line_atts()
            ps.print_for_loop( [ Option[0] for Option in self.OPTIONS.values() ] )
            choice, user_input = self.RTI.get_one_input()

            if choice != None:
                self.run_RTI_choice( choice )
                continue

            if user_input == '':
                break

            try:
                user_input = int(user_input)
            except:
                continue

            if user_input in self.OPTIONS:
                self.run_method( self.OPTIONS[user_input][-1] )

        self.exit()

    def exit( self ):

        pass
