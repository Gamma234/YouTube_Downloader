

from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL
from data.tools.YouTube_DLer_v5 import Audio_Video_Handler as AVHD

import tkinter.scrolledtext as tkscrolled
import tkinter as tk

def show_url_info_in_Combine_an_audio_stream_and_a_video_stream( mgmt, main_mgmt, data ) :

    mgmt['warning_label'].pack_forget()
    mgmt['combine_warning_label'].pack_forget()
    mgmt['url_button'].config( state=tk.DISABLED )

    try :
        mgmt['warning_label'].pack( side=tk.LEFT, padx=5 )
        mgmt['warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
        main_mgmt['main_window'].update()

        data['url_info'] = YTDL.get_url_information( url= mgmt['url_entry'].get(),
                                                     show_dict={ 'show details' : True,
                                                                 'only audio' : True,
                                                                 'only video' : True } )

        GT.write_text( mgmt['display_info_text'], data['url_info']['information'],
                       fg='SystemWindowText', to_bottom=False )

        data['audio_itag_list'] = [ 'None' ] + data['url_info'].get_streams_itag( target_key='only audio' )
        GT.refresh_optionMenu( mgmt['audio_strVar'], mgmt['audio_optMn'], data['audio_itag_list'] )

        data['video_itag_list'] = [ 'None' ] + data['url_info'].get_streams_itag( target_key='only video' )
        GT.refresh_optionMenu( mgmt['video_strVar'], mgmt['video_optMn'], data['video_itag_list'] )

        mgmt['warning_label'].config( text='Done', fg='green' )
    except Exception as e :

        GT.write_text( mgmt['display_info_text'], '[ERROR]\n' + str( e ), fg='red' )

        data['audio_itag_list'] = [ 'None' ]
        GT.refresh_optionMenu( mgmt['audio_strVar'], mgmt['audio_optMn'], data['audio_itag_list'] )

        data['video_itag_list'] = [ 'None' ]
        GT.refresh_optionMenu( mgmt['video_strVar'], mgmt['video_optMn'], data['video_itag_list'] )

        mgmt['warning_label'].pack_forget()
        mgmt['combine_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['url_button'].config( state=tk.NORMAL ) ) 

def change_target_info_in_Combine_an_audio_stream_and_a_video_stream( mgmt, data ) :

    mgmt['combine_warning_label'].pack_forget()

    target_str = ''
    audio_str, video_str =  mgmt['audio_strVar'].get(), mgmt['video_strVar'].get()

    target_str = target_str + '------target audio-------------\n'
    target_str = target_str + ( str( data['url_info'].get_stream_by_itag( audio_str ) ) 
                                if ( audio_str != 'None' and audio_str != '' ) else 'None' ) + '\n'
    target_str = target_str + '---------------------------------\n\n'

    target_str = target_str + '------target video--------------\n'
    target_str = target_str + ( str( data['url_info'].get_stream_by_itag( video_str ) ) 
                                if ( video_str != 'None' and video_str != '' ) else 'None' ) + '\n'
    target_str = target_str + '---------------------------------\n'

    GT.write_text( mgmt['target_info_text'], target_str, fg='SystemWindowText' )

def combine_in_Combine_an_audio_stream_and_a_video_stream( mgmt, main_mgmt, data ) :

    mgmt['combine_warning_label'].pack_forget()
    mgmt['combine_button'].config( state=tk.DISABLED )

    try :
        running = True

        if running and main_mgmt['download_boolVar'].get() == False :
            mgmt['combine_warning_label'].config( text='Download OFF', fg='red' )
            mgmt['combine_warning_label'].pack( side=tk.LEFT, padx=5 )
            running = False

        if running and main_mgmt['save_path_entry']['highlightbackground'] != 'green' :
            mgmt['combine_warning_label'].config( text='Invalid Save Path', fg='red' )
            mgmt['combine_warning_label'].pack( side=tk.LEFT, padx=5 )
            running = False

        if running :

            audio_str, video_str =  mgmt['audio_strVar'].get(), mgmt['video_strVar'].get()

            if audio_str == 'None' or video_str == 'None' :
                GT.write_text( mgmt['target_info_text'], '[ERROR]\n' + 'Combine "None" streams !', fg='red' )
                mgmt['combine_warning_label'].pack_forget()
            else :
                mgmt['combine_warning_label'].pack( side=tk.LEFT, padx=5 )
                mgmt['combine_warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
                main_mgmt['main_window'].update()

                AVHD.combine_audio_video( audio_strm=data['url_info'].get_stream_by_itag( audio_str ),
                                          video_strm=data['url_info'].get_stream_by_itag( video_str ),
                                          title=data['url_info']['title'],
                                          save_path= main_mgmt['save_path_strVar'].get(),
                                          download=main_mgmt['download_boolVar'].get() )

                mgmt['combine_warning_label'].config( text='Done', fg='green' )
                mgmt['combine_warning_label'].pack( side=tk.LEFT, padx=5 )
            
    except Exception as e :
        GT.write_text( mgmt['target_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['combine_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['combine_button'].config( state=tk.NORMAL ) ) 

def Combine_an_audio_stream_and_a_video_stream( main_frame, main_mgmt, main_conf ) :

    ret_mgmt = {} ## empty dictionary
    data = {} ## empty dictionary

    ### add frame

    ret_mgmt['input_frame'] = tk.Frame( main_frame )
    ret_mgmt['input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['display_frame'] = tk.Frame( main_frame )
    ret_mgmt['display_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['combine_frame'] = tk.Frame( main_frame )
    ret_mgmt['combine_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['target_frame'] = tk.Frame( main_frame )
    ret_mgmt['target_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ### set on "ret_mgmt['input_frame']"

    ret_mgmt['url_label'] = tk.Label( ret_mgmt['input_frame'], text='URL :' )
    ret_mgmt['url_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_entry'] = tk.Entry( ret_mgmt['input_frame'], width=70 )
    ret_mgmt['url_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['url_button'] = tk.Button( ret_mgmt['input_frame'], text='GET',
                                        command=( lambda : show_url_info_in_Combine_an_audio_stream_and_a_video_stream( ret_mgmt, main_mgmt, data ) ) )
    ret_mgmt['url_button'].pack( side=tk.LEFT )

    ret_mgmt['warning_label'] = tk.Label( ret_mgmt['input_frame'], text='', fg='green' )

    ### set on "ret_mgmt['display_frame']"

    ret_mgmt['display_label'] = tk.Label( ret_mgmt['display_frame'], text='Information :' )
    ret_mgmt['display_label'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['display_info_text'] = tkscrolled.ScrolledText( ret_mgmt['display_frame'], width=120, height=20, state=tk.DISABLED )
    ret_mgmt['display_info_text'].pack( padx=10, anchor=tk.NW )

    ### set on "ret_mgmt['combine_frame']"

    ret_mgmt['audio_label'] = tk.Label( ret_mgmt['combine_frame'], text='Audio itag :' )
    ret_mgmt['audio_label'].pack( side=tk.LEFT, padx=5 )

    data['audio_itag_list'] = [ 'None' ]

    ret_mgmt['audio_strVar'] = tk.StringVar( ret_mgmt['combine_frame'] )
    ret_mgmt['audio_strVar'].set( data['audio_itag_list'][0] )

    ret_mgmt['audio_optMn'] = tk.OptionMenu( ret_mgmt['combine_frame'], ret_mgmt['audio_strVar'], *data['audio_itag_list'] )
    ret_mgmt['audio_optMn'].config( width=10 )
    ret_mgmt['audio_optMn'].pack( side=tk.LEFT )

    ret_mgmt['audio_strVar'].trace( "w", lambda arg1, arg2, arg3 : change_target_info_in_Combine_an_audio_stream_and_a_video_stream( ret_mgmt, data ) ) ## monitor

    ret_mgmt['video_label'] = tk.Label( ret_mgmt['combine_frame'], text='Video itag :' )
    ret_mgmt['video_label'].pack( side=tk.LEFT, padx=5 )

    data['video_itag_list'] = [ 'None' ]

    ret_mgmt['video_strVar'] = tk.StringVar( ret_mgmt['combine_frame'] )
    ret_mgmt['video_strVar'].set( data['video_itag_list'][0] )

    ret_mgmt['video_optMn'] = tk.OptionMenu( ret_mgmt['combine_frame'], ret_mgmt['video_strVar'], *data['video_itag_list'] )
    ret_mgmt['video_optMn'].config( width=10 )
    ret_mgmt['video_optMn'].pack( side=tk.LEFT )

    ret_mgmt['video_strVar'].trace( "w", lambda arg1, arg2, arg3 : change_target_info_in_Combine_an_audio_stream_and_a_video_stream( ret_mgmt, data ) ) ## monitor

    ret_mgmt['combine_button'] = tk.Button( ret_mgmt['combine_frame'], text='Combine', bg='yellow',
                                             command=( lambda : combine_in_Combine_an_audio_stream_and_a_video_stream( ret_mgmt, main_mgmt, data ) ) )
    ret_mgmt['combine_button'].pack( side=tk.LEFT, padx=30 )

    ret_mgmt['combine_warning_label'] = tk.Label( ret_mgmt['combine_frame'], text='', fg='red' )

    ### set on "ret_mgmt['target_frame']"

    ret_mgmt['target_label'] = tk.Label( ret_mgmt['target_frame'], text='Target information :' )
    ret_mgmt['target_label'].pack( padx=5, anchor=tk.NW )

    ret_mgmt['target_info_text'] = tkscrolled.ScrolledText( ret_mgmt['target_frame'], width=120, height=10, state=tk.DISABLED )
    ret_mgmt['target_info_text'].pack( padx=10, anchor=tk.NW )

    return ret_mgmt



