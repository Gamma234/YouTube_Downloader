
from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL

import tkinter.scrolledtext as tkscrolled
import tkinter as tk

def show_url_info_in_Single_Download( mgmt, main_mgmt, data ) :

    mgmt['get_warning_label'].pack_forget()
    mgmt['download_warning_label'].pack_forget()
    mgmt['url_button'].config( state=tk.DISABLED )

    try :
        show_dict = {}

        mgmt['get_warning_label'].pack( side=tk.LEFT, padx=5 )
        mgmt['get_warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
        main_mgmt['main_window'].update()

        for key in mgmt['chk_val_dict'].keys() :
            show_dict[key] = mgmt['chk_val_dict'][key].get()

        data['url_info'] = YTDL.get_url_information( url= mgmt['url_entry'].get(), show_dict=show_dict )

        GT.write_text( mgmt['display_info_text'], data['url_info']['information'], fg='SystemWindowText' )

        data['code_list'] = [ 'None' ] + data['url_info'].get_captions_code()
        GT.refresh_optionMenu( mgmt['code_strVar'], mgmt['code_optMn'], data['code_list'] )

        data['itag_list'] = [ 'None' ] + data['url_info'].get_streams_itag()
        GT.refresh_optionMenu( mgmt['itag_strVar'], mgmt['itag_optMn'], data['itag_list'] )

        mgmt['get_warning_label'].config( text='Done', fg='green' )
    except Exception as e :

        GT.write_text( mgmt['display_info_text'], '[ERROR]\n' + str( e ), fg='red' )

        data['code_list'] = [ 'None' ]
        GT.refresh_optionMenu( mgmt['code_strVar'], mgmt['code_optMn'], data['code_list'] )

        data['itag_list'] = [ 'None' ]
        GT.refresh_optionMenu( mgmt['itag_strVar'], mgmt['itag_optMn'], data['itag_list'] )

        mgmt['get_warning_label'].pack_forget()
        mgmt['download_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['url_button'].config( state=tk.NORMAL ) ) 

def change_target_info_in_Single_Download( mgmt, data ) :

    mgmt['download_warning_label'].pack_forget()

    target_str = ''
    code_str, itag_str =  mgmt['code_strVar'].get(), mgmt['itag_strVar'].get()

    target_str = target_str + '------target caption-------------\n'
    target_str = target_str + ( str( data['url_info'].get_caption_by_code( code_str ) ) 
                                if ( code_str != 'None' and code_str != '' ) else 'None' ) + '\n'
    target_str = target_str + '---------------------------------\n\n'

    target_str = target_str + '------target stream--------------\n'
    target_str = target_str + ( str( data['url_info'].get_stream_by_itag( itag_str ) ) 
                                if ( itag_str != 'None' and itag_str != '' ) else 'None' ) + '\n'
    target_str = target_str + '---------------------------------\n'

    GT.write_text( mgmt['target_info_text'], target_str, fg='SystemWindowText' )

def download_in_Single_Download( mgmt, main_mgmt, data ) :

    mgmt['download_warning_label'].pack_forget()
    mgmt['download_button'].config( state=tk.DISABLED )

    try :
        if main_mgmt['download_boolVar'].get() == True :
            
            if main_mgmt['save_path_entry']['highlightbackground'] == 'green' :

                mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )
                mgmt['download_warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
                main_mgmt['main_window'].update()
            
                code_str, itag_str =  mgmt['code_strVar'].get(), mgmt['itag_strVar'].get()

                if code_str != 'None' :
                    YTDL.download_caption( cap=data['url_info'].get_caption_by_code( code_str ),
                                           title=data['url_info']['title'],
                                           save_path=main_mgmt['save_path_strVar'].get(),
                                           download=main_mgmt['download_boolVar'].get() )

                if itag_str != 'None' :
                    YTDL.download_stream( strm=data['url_info'].get_stream_by_itag( itag_str ),
                                          save_path=main_mgmt['save_path_strVar'].get(),
                                          download=main_mgmt['download_boolVar'].get() )

                mgmt['download_warning_label'].config( text='Done', fg='green' )
                mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )
            else :
                mgmt['download_warning_label'].config( text='Invalid Save Path', fg='red' )
                mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )

        else :
            mgmt['download_warning_label'].config( text='Download OFF', fg='red' )
            mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )
    except Exception as e :
        GT.write_text( mgmt['target_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['download_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['download_button'].config( state=tk.NORMAL ) ) 

def Single_Download( main_frame, main_mgmt, main_conf ) :

    ret_mgmt = {} ## empty dictionary
    data = {} ## empty dictionary

    ### add frame

    ret_mgmt['input_frame'] = tk.Frame( main_frame )
    ret_mgmt['input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['options_frame'] = tk.Frame( main_frame, height=50 )
    ret_mgmt['options_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['display_frame'] = tk.Frame( main_frame )
    ret_mgmt['display_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['select_frame'] = tk.Frame( main_frame )
    ret_mgmt['select_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['target_frame'] = tk.Frame( main_frame )
    ret_mgmt['target_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ### set on "ret_mgmt['input_frame']"

    ret_mgmt['url_label'] = tk.Label( ret_mgmt['input_frame'], text='URL :' )
    ret_mgmt['url_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_entry'] = tk.Entry( ret_mgmt['input_frame'], width=70 )
    ret_mgmt['url_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_button'] = tk.Button( ret_mgmt['input_frame'], text='GET',
                                        command=( lambda : show_url_info_in_Single_Download( ret_mgmt, main_mgmt, data ) ) )
    ret_mgmt['url_button'].pack( side=tk.LEFT )

    ret_mgmt['get_warning_label'] = tk.Label( ret_mgmt['input_frame'], text='', fg='green' )

    ### set on "ret_mgmt['options_frame']"

    options_name = [ 'show details', 'show captions', 'show streams',
                     'only audio', 'only video', 'show progressive' ]
    
    ret_mgmt['chk_val_dict'] = { 'show details' : tk.BooleanVar( value=True ),
                                 'show captions' : tk.BooleanVar( value=True ),
                                 'show streams' : tk.BooleanVar( value=False ),
                                 'only audio' : tk.BooleanVar( value=False ),
                                 'only video' : tk.BooleanVar( value=False ),
                                 'show progressive' : tk.BooleanVar( value=True ) }

    for key in options_name :
        ret_mgmt[key] = tk.Checkbutton( ret_mgmt['options_frame'], text=key, var=ret_mgmt['chk_val_dict'][key] ) 
        ret_mgmt[key].pack( side=tk.LEFT )

    ### set on "ret_mgmt['display_frame']"

    ret_mgmt['display_label'] = tk.Label( ret_mgmt['display_frame'], text='Information :' )
    ret_mgmt['display_label'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['display_info_text'] = tkscrolled.ScrolledText( ret_mgmt['display_frame'], width=120, height=15, state=tk.DISABLED )
    ret_mgmt['display_info_text'].pack( padx=10, anchor=tk.NW )

    ### set on "ret_mgmt['select_frame']"

    ret_mgmt['code_label'] = tk.Label( ret_mgmt['select_frame'], text='Select a caption :' )
    ret_mgmt['code_label'].pack( side=tk.LEFT, padx=5 )

    data['code_list'] = [ 'None' ]

    ret_mgmt['code_strVar'] = tk.StringVar( ret_mgmt['select_frame'] )
    ret_mgmt['code_strVar'].set( data['code_list'][0] )

    ret_mgmt['code_optMn'] = tk.OptionMenu( ret_mgmt['select_frame'], ret_mgmt['code_strVar'], *data['code_list'] )
    ret_mgmt['code_optMn'].config( width=10 )
    ret_mgmt['code_optMn'].pack( side=tk.LEFT )

    ret_mgmt['code_strVar'].trace( "w", lambda arg1, arg2, arg3 : change_target_info_in_Single_Download( ret_mgmt, data ) ) ## monitor

    ret_mgmt['itag_label'] = tk.Label( ret_mgmt['select_frame'], text='Select an itag :' )
    ret_mgmt['itag_label'].pack( side=tk.LEFT, padx=5 )

    data['itag_list'] = [ 'None' ]

    ret_mgmt['itag_strVar'] = tk.StringVar( ret_mgmt['select_frame'] )
    ret_mgmt['itag_strVar'].set( data['itag_list'][0] )

    ret_mgmt['itag_optMn'] = tk.OptionMenu( ret_mgmt['select_frame'], ret_mgmt['itag_strVar'], *data['itag_list'] )
    ret_mgmt['itag_optMn'].config( width=10 )
    ret_mgmt['itag_optMn'].pack( side=tk.LEFT )

    ret_mgmt['itag_strVar'].trace( "w", lambda arg1, arg2, arg3 : change_target_info_in_Single_Download( ret_mgmt, data ) ) ## monitor

    ret_mgmt['download_button'] = tk.Button( ret_mgmt['select_frame'], text='Download', bg='yellow',
                                             command=( lambda : download_in_Single_Download( ret_mgmt, main_mgmt, data ) ) )
    ret_mgmt['download_button'].pack( side=tk.LEFT, padx=30 )

    ret_mgmt['download_warning_label'] = tk.Label( ret_mgmt['select_frame'], text='', fg='red' )

    ### set on "ret_mgmt['target_frame']"

    ret_mgmt['target_label'] = tk.Label( ret_mgmt['target_frame'], text='Target information :' )
    ret_mgmt['target_label'].pack( padx=5, anchor=tk.NW )

    ret_mgmt['target_info_text'] = tkscrolled.ScrolledText( ret_mgmt['target_frame'], width=120, height=10, state=tk.DISABLED )
    ret_mgmt['target_info_text'].pack( padx=10, anchor=tk.NW )

    return ret_mgmt

