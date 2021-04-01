
from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL

import tkinter.scrolledtext as tkscrolled
import tkinter as tk


def show_url_info_in_Print_Information( mgmt, main_mgmt ) :

    mgmt['get_warning_label'].pack_forget()
    mgmt['url_button'].config( state=tk.DISABLED )

    try :
        show_dict = {}

        mgmt['get_warning_label'].pack( side=tk.LEFT, padx=5 )
        mgmt['get_warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
        main_mgmt['main_window'].update()

        for key in mgmt['chk_val_dict'].keys() :
            show_dict[key] = mgmt['chk_val_dict'][key].get()

        url_info = YTDL.get_url_information( url= mgmt['url_entry'].get(), show_dict=show_dict )

        GT.write_text( mgmt['display_info_text'], url_info['information'], fg='SystemWindowText' )

        mgmt['get_warning_label'].config( text='Done', fg='green' )
    except Exception as e :
        GT.write_text( mgmt['display_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['get_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['url_button'].config( state=tk.NORMAL ) ) 

def Print_Information( main_frame, main_mgmt, main_conf ) :

    ret_mgmt = {} ## empty dictionary

    ### add frame

    ret_mgmt['input_frame'] = tk.Frame( main_frame )
    ret_mgmt['input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['options_frame'] = tk.Frame( main_frame, height=50 )
    ret_mgmt['options_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['display_frame'] = tk.Frame( main_frame )
    ret_mgmt['display_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ### set on "ret_mgmt['input_frame']"

    ret_mgmt['url_label'] = tk.Label( ret_mgmt['input_frame'], text='URL :' )
    ret_mgmt['url_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_entry'] = tk.Entry( ret_mgmt['input_frame'], width=70 )
    ret_mgmt['url_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_button'] = tk.Button( ret_mgmt['input_frame'], text='GET',
                                        command=( lambda : show_url_info_in_Print_Information( ret_mgmt, main_mgmt ) ) )
    ret_mgmt['url_button'].pack( side=tk.LEFT )

    ret_mgmt['get_warning_label'] = tk.Label( ret_mgmt['input_frame'], text='', fg='green' )

    ### set on "ret_mgmt['options_frame']"

    options_name = [ 'show details', 'show captions', 'show streams',
                     'only audio', 'only video', 'show progressive' ]
    
    ret_mgmt['chk_val_dict'] = { 'show details' : tk.BooleanVar( value=True ),
                                 'show captions' : tk.BooleanVar( value=True ),
                                 'show streams' : tk.BooleanVar( value=True ),
                                 'only audio' : tk.BooleanVar( value=True ),
                                 'only video' : tk.BooleanVar( value=True ),
                                 'show progressive' : tk.BooleanVar( value=True ) }

    for key in options_name :
        ret_mgmt[key] = tk.Checkbutton( ret_mgmt['options_frame'], text=key, var=ret_mgmt['chk_val_dict'][key] ) 
        ret_mgmt[key].pack( side=tk.LEFT )

    ### set on "ret_mgmt['display_frame']"

    ret_mgmt['display_label'] = tk.Label( ret_mgmt['display_frame'], text='Information :' )
    ret_mgmt['display_label'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['display_info_text'] = tkscrolled.ScrolledText( ret_mgmt['display_frame'], width=120, height=25, state=tk.DISABLED )
    ret_mgmt['display_info_text'].pack( padx=10, anchor=tk.NW )

    return ret_mgmt

