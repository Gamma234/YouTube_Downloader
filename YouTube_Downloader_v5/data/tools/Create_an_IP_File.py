
from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL

import tkinter.scrolledtext as tkscrolled
import tkinter as tk
import os

def create_in_Create_an_IP_File( mgmt, main_mgmt ) :

    mgmt['warning_label'].pack_forget()
    mgmt['create_button'].config( state=tk.DISABLED )

    try :
        running = True

        if running and main_mgmt['download_boolVar'].get() == False :
            mgmt['warning_label'].config( text='Download OFF', fg='red' )
            mgmt['warning_label'].pack( side=tk.LEFT, padx=5 )
            running = False

        if running and main_mgmt['save_path_entry']['highlightbackground'] != 'green' :
            mgmt['warning_label'].config( text='Invalid Save Path', fg='red' )
            mgmt['warning_label'].pack( side=tk.LEFT, padx=5 )
            running = False

        if running and mgmt['file_entry']['highlightbackground'] != 'green' :
            mgmt['warning_label'].config( text='Invalid Output File Name', fg='red' )
            mgmt['warning_label'].pack( side=tk.LEFT, padx=5 )
            running = False

        if running :
            url_list = YTDL.get_playlist_urls( mgmt['playlist_url_entry'].get() )
            out_file = main_mgmt['save_path_entry'].get() + '\\' + mgmt['file_entry'].get()

            result_str = 'Total URLs : ' + str( len( url_list ) ) + '\n'
            result_str = result_str + 'Output File Name : ' + out_file + '\n\n'
            result_str = result_str + '---------------------------------\n'
            for url in url_list :
                result_str = result_str + url + '\n'
            result_str = result_str + '---------------------------------\n\n'

            YTDL.create_ip_file( playlist_url=mgmt['playlist_url_entry'].get(), 
                                 save_path=main_mgmt['save_path_entry'].get(), 
                                 file_name=mgmt['file_entry'].get() )

            GT.write_text( mgmt['display_info_text'], result_str, fg='SystemWindowText' )

            mgmt['warning_label'].config( text='Done', fg='green' )
            mgmt['warning_label'].pack( side=tk.LEFT, padx=5 )

    except Exception as e :
        GT.write_text( mgmt['display_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        
    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['create_button'].config( state=tk.NORMAL ) ) 

def check_output_file_in_Create_an_IP_File( mgmt, main_mgmt ) :

    mgmt['warning_label'].pack_forget()
    output_file_name = mgmt['file_strVar'].get()

    if mgmt['file_entry']['highlightbackground'] == 'green' :
        if ( output_file_name != '' ) and ( not output_file_name.isspace() ) :
            pass
        else :
            mgmt['file_entry'].config( highlightbackground='red', highlightcolor='red' )
    else :
        if ( output_file_name != '' ) and ( not output_file_name.isspace() ) :
            mgmt['file_entry'].config( highlightbackground='green', highlightcolor='green' )
        else :
            pass

def Create_an_IP_File( main_frame, main_mgmt, main_conf ) :
    
    ret_mgmt = {} ## empty dictionary

    ### add frame

    ret_mgmt['input_frame'] = tk.Frame( main_frame )
    ret_mgmt['input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['file_frame'] = tk.Frame( main_frame )
    ret_mgmt['file_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['display_frame'] = tk.Frame( main_frame )
    ret_mgmt['display_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ### set on "ret_mgmt['input_frame']"

    ret_mgmt['playlist_url_label'] = tk.Label( ret_mgmt['input_frame'], text='Playlist URL :' )
    ret_mgmt['playlist_url_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['playlist_url_entry'] = tk.Entry( ret_mgmt['input_frame'], width=90 )
    ret_mgmt['playlist_url_entry'].pack( side=tk.LEFT, padx=5 )

    ### set on "ret_mgmt['file_frame']"

    ret_mgmt['file_label'] = tk.Label( ret_mgmt['file_frame'], text='Output File :' )
    ret_mgmt['file_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['file_strVar'] = tk.StringVar()
    ret_mgmt['file_entry'] = tk.Entry( ret_mgmt['file_frame'], width=30, textvariable=ret_mgmt['file_strVar'],
                                       highlightthickness=2, highlightbackground='green', highlightcolor='green' )
    ret_mgmt['file_entry'].pack( side=tk.LEFT, padx=5 )
    ret_mgmt['file_strVar'].set( 'ip_file.txt' )

    ret_mgmt['file_strVar'].trace( 'w', lambda arg1, arg2, arg3 : check_output_file_in_Create_an_IP_File( ret_mgmt, main_mgmt ) ) ## monitor

    ret_mgmt['create_button'] = tk.Button( ret_mgmt['file_frame'], text='Create', bg='yellow',
                                           command=( lambda : create_in_Create_an_IP_File( ret_mgmt, main_mgmt ) ) )
    ret_mgmt['create_button'].pack( side=tk.LEFT )

    ret_mgmt['warning_label'] = tk.Label( ret_mgmt['file_frame'], text='', fg='green' )

    ### set on "ret_mgmt['display_frame']"

    ret_mgmt['display_label'] = tk.Label( ret_mgmt['display_frame'], text='Information :' )
    ret_mgmt['display_label'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['display_info_text'] = tkscrolled.ScrolledText( ret_mgmt['display_frame'], width=120, height=30, state=tk.DISABLED )
    ret_mgmt['display_info_text'].pack( padx=10, anchor=tk.NW )

    return ret_mgmt




