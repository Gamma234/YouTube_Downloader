
import tkinter as tk

class Global_Tools() :

    def __init__( self ) :
        pass

    @staticmethod
    def all_destroy( mgmt ) :

        if isinstance( mgmt, dict ) :

            for key in mgmt.keys() :
                try : 
                    if isinstance( mgmt[key], dict ) or isinstance( mgmt[key], list ) :
                        self.all_destroy( mgmt[key] )
                    else :
                        mgmt[key].destroy()
                except : 
                    pass

        elif isinstance( mgmt, list ) :

            for element in mgmt :
                try : 
                    if isinstance( element, dict ) or isinstance( element, list ) :
                        self.all_destroy( element )
                    else :
                        element.destroy()
                except : 
                    pass

        else :
            pass

    @staticmethod
    def show_error( window, error_msg ) :

        error_window = tk.Toplevel( window )
        error_window.title( 'Error Message' ) 
        error_window.geometry( '200x50' )
        tk.Label( error_window, text=( '[ERROR]\n' + error_msg ) ).pack()
        error_window.grab_set()

    @staticmethod
    def write_text( text_window, msg, fg='SystemWindowText', replace=True, to_bottom=False ) :

        text_window.config( state=tk.NORMAL, fg=fg )

        if replace :
            text_window.delete( 1.0, tk.END )
            text_window.insert( 1.0, msg )
        else :
            text_window.insert( tk.END, msg )

        if to_bottom :
            text_window.yview( tk.END )
        
        text_window.config( state=tk.DISABLED )

    @staticmethod
    def refresh_optionMenu( var, option_menu, new_option_list ) :

        var.set( '' )
        option_menu['menu'].delete( 0, 'end' )

        for opt in new_option_list:
            option_menu['menu'].add_command( label=opt, command=tk._setit( var, opt ) )

        var.set( new_option_list[0] )


