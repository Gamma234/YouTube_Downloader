
from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL

import tkinter.scrolledtext as tkscrolled
import tkinter.filedialog as filedlg
import tkinter as tk
import os

from data.tools.See_Information import *


def handle_stream_in_Download_From_a_File( url, mgmt, main_mgmt, data ) :

    filter_dict = {}
    info = 'stream\n---------------------------------\n'
    success = True
    strm = None

    for key in mgmt['chk_val_dict']['filter_dict'].keys() :
        if mgmt['chk_val_dict']['filter_dict'][key].get() == True :
            if key in data['input_opt_default_dict'].keys() :
                filter_dict[key] = mgmt[key + '_entry'].get()
            else :
                filter_dict[key] = True
        else :
            filter_dict[key] = None

    try :
        strm = YTDL.get_stream_by_filter( url, filter_dict )
        info = info + str( strm ) + '\n---------------------------------\n'
    except Exception as e :
        success = False
        info = info + 'ERROR : ' + str( e ) + '\n---------------------------------\n'

    GT.write_text( mgmt['show_info_text'], info, fg='SystemWindowText', replace=False, to_bottom=True )
    main_mgmt['main_window'].update()

    if strm == None or success == False :
        GT.write_text( mgmt['show_info_text'], '\nFail\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
        main_mgmt['main_window'].update()
        return False
    else :
        try :

            YTDL.download_stream( strm=strm,
                                  save_path=main_mgmt['save_path_strVar'].get(),
                                  download=main_mgmt['download_boolVar'].get() )

            GT.write_text( mgmt['show_info_text'], '\nDone\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
            main_mgmt['main_window'].update()
            return True
        except Exception as e :
            GT.write_text( mgmt['show_info_text'], '\nFail\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
            main_mgmt['main_window'].update()
            return False

def handle_caption_in_Download_From_a_File( url, mgmt, main_mgmt, data ) :

    caption = mgmt['caption_entry'].get() if mgmt['chk_val_dict']['caption'].get() == True else None

    if caption == None :
        return None

    cap = None
    title = None
    success = True
    info = 'caption\n---------------------------------\n'

    try :
        url_info = YTDL.get_url_information( url=url, show_dict={ 'show details' : True,
                                                                  'show captions' : True } )
        cap = url_info.get_caption_by_code( caption )
        title = url_info['title']
        info = info + str( cap ) + '\n---------------------------------\n'
    except Exception as e :
        success = False
        info = info + 'ERROR : ' + str( e ) + '\n---------------------------------\n'

    GT.write_text( mgmt['show_info_text'], info, fg='SystemWindowText', replace=False, to_bottom=True )
    main_mgmt['main_window'].update()

    if cap == None or success == False :
        GT.write_text( mgmt['show_info_text'], '\nFail\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
        main_mgmt['main_window'].update()
        return False
    else :
        try :

            YTDL.download_caption( cap=cap,
                                   title=title,
                                   save_path=main_mgmt['save_path_strVar'].get(),
                                   download=main_mgmt['download_boolVar'].get() )

            GT.write_text( mgmt['show_info_text'], '\nDone\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
            main_mgmt['main_window'].update()
            return True
        except Exception as e :
            GT.write_text( mgmt['show_info_text'], '\nFail\n\n', fg='SystemWindowText', replace=False, to_bottom=True )
            main_mgmt['main_window'].update()
            return False

def download_in_Download_From_a_File( mgmt, main_mgmt, data ) :

    mgmt['download_warning_label'].pack_forget()
    mgmt['download_button'].config( state=tk.DISABLED )
    GT.write_text( mgmt['show_info_text'], '', fg='SystemWindowText' )

    try :
        running = True

        if running and main_mgmt['download_boolVar'].get() == False :
            GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + 'Download OFF', fg='red' )
            mgmt['download_warning_label'].pack_forget()
            running = False

        if running and main_mgmt['save_path_entry']['highlightbackground'] != 'green' :
            GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + 'Invalid Save Path', fg='red' )
            mgmt['download_warning_label'].pack_forget()
            running = False

        if running and mgmt['file_entry']['highlightbackground'] != 'green' :
            GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + 'Invalid File Name', fg='red' )
            mgmt['download_warning_label'].pack_forget()
            running = False

        if running :
            mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )
            mgmt['download_warning_label'].config( text='Please wait ...', fg='SystemWindowText' )
            main_mgmt['main_window'].update()

            ip_file = open( mgmt['file_entry'].get(), 'r' )
            warning_str = ''
            num = 1 
            strm_cond, cap_cond = None, None
            strm_done, strm_fail = 0, 0
            cap_done, cap_fail = 0, 0

            for url in ip_file.readlines() :

                if url.isspace() :
                    continue

                GT.write_text( mgmt['show_info_text'],
                                '[' + str( num ) + ']\n' + url.rstrip() + '\n\n',
                                fg='SystemWindowText', replace=False, to_bottom=True )
                main_mgmt['main_window'].update()

                if mgmt['chk_val_dict']['only_caption'].get() == False :
                    strm_cond = handle_stream_in_Download_From_a_File( url, mgmt, main_mgmt, data )
                cap_cond = handle_caption_in_Download_From_a_File( url, mgmt, main_mgmt, data )                    

                if strm_cond == True :
                    strm_done += 1
                else :
                    strm_fail += 1

                if cap_cond == None :
                    cap_done, cap_fail = None, None
                elif cap_cond == True :
                    cap_done += 1
                else :
                    cap_fail += 1

                GT.write_text( mgmt['show_info_text'], '\n', fg='SystemWindowText', replace=False, to_bottom=True )
                main_mgmt['main_window'].update()
                num += 1

            ip_file.close()

            if strm_cond == None :
                warning_str = '( only_caption )'
            else :
                warning_str = ( 'stream : [ Done : ' + str( strm_done ) + '  Fail : ' + str( strm_fail ) + ']' )

            if cap_done != None :
                warning_str = warning_str + '\n' + ( 'caption : [ Done : ' + str( cap_done ) + '  Fail : ' + str( cap_fail ) + ']' )

            mgmt['download_warning_label'].config( text=warning_str, fg='green' )
            mgmt['download_warning_label'].pack( side=tk.LEFT, padx=5 )

    except Exception as e :
        GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['download_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['download_button'].config( state=tk.NORMAL ) ) 

def see_info_in_Download_From_a_File( mgmt, main_mgmt ) :

    mgmt['download_warning_label'].pack_forget()
    mgmt['see_info_button'].config( state=tk.DISABLED )
    GT.write_text( mgmt['show_info_text'], '', fg='SystemWindowText' )

    try :

        if mgmt['file_entry']['highlightbackground'] == 'green' :

            url_list = ['None']
            ip_file = open( mgmt['file_entry'].get(), 'r' )

            for url in ip_file.readlines() :
                if not url.isspace() :
                    url_list.append( url )

            ip_file.close()

            See_Information( url_list, main_mgmt )

        else :
            GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + 'Invalid File Name', fg='red' )
            mgmt['download_warning_label'].pack_forget()

    except Exception as e :
        GT.write_text( mgmt['show_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['download_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['see_info_button'].config( state=tk.NORMAL ) ) 

def select_file_in_Download_From_a_File( mgmt, main_mgmt ) :

    mgmt['file_strVar'].set( filedlg.askopenfilename() )
    mgmt['file_entry'].xview( tk.END )

def check_file_in_Download_From_a_File( mgmt, main_mgmt ) :

    if mgmt['file_entry']['highlightbackground'] == 'green' :
        if os.path.isfile( mgmt['file_strVar'].get() ) :
            pass
        else :
            mgmt['file_entry'].config( highlightbackground='red', highlightcolor='red' )
    else :
        if os.path.isfile( mgmt['file_strVar'].get() ) :
            mgmt['file_entry'].config( highlightbackground='green', highlightcolor='green' )
        else :
            pass

def check_ability_in_Download_From_a_File( mgmt ) :

    def change( mgmt, state, ignore ) :
        for k in mgmt['chk_val_dict']['filter_dict'].keys() :
            if not ( k in ignore ) :
                mgmt[k].config( state=state )

    if mgmt['chk_val_dict']['only_caption'].get() == True :
        mgmt['chk_val_dict']['caption'].set( True )
        mgmt['caption'].config( state=tk.DISABLED, disabledforeground='SystemWindowText' )
        change( mgmt, tk.DISABLED, [] )
    else :
        mgmt['caption'].config( state=tk.NORMAL )
        change( mgmt, tk.NORMAL, [] )

        if mgmt['chk_val_dict']['filter_dict']['itag'].get() == True :
            change( mgmt, tk.DISABLED, ['itag'] )
        elif mgmt['chk_val_dict']['filter_dict']['highest'].get() == True :
            change( mgmt, tk.DISABLED, ['highest'] )
        else :
            pass    

def Download_From_a_File( main_frame, main_mgmt, main_conf ) :
    
    ret_mgmt = {} ## empty dictionary
    data = {} ## empty dictionary

    ### add frame

    ret_mgmt['up_frame'] = tk.Frame( main_frame )
    ret_mgmt['up_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['down_frame'] = tk.Frame( main_frame )
    ret_mgmt['down_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )    

    ### set on "ret_mgmt['up_frame']"

    ret_mgmt['file_label'] = tk.Label( ret_mgmt['up_frame'], text='File Name :' )
    ret_mgmt['file_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['file_strVar'] = tk.StringVar()
    ret_mgmt['file_strVar'].set( 'ip_file.txt' )

    ret_mgmt['file_entry'] = ( tk.Entry( ret_mgmt['up_frame'], width=50, textvariable=ret_mgmt['file_strVar'],
                                         highlightthickness=2, highlightbackground='green', highlightcolor='green' ) 
                               if os.path.isfile( ret_mgmt['file_strVar'].get() ) else
                               tk.Entry( ret_mgmt['up_frame'], width=50, textvariable=ret_mgmt['file_strVar'],
                                         highlightthickness=2, highlightbackground='red', highlightcolor='red' ) )
    ret_mgmt['file_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['file_strVar'].trace( 'w', lambda arg1, arg2, arg3 : check_file_in_Download_From_a_File( ret_mgmt, main_mgmt ) ) ## monitor

    ret_mgmt['select_button'] = tk.Button( ret_mgmt['up_frame'], text='Select File',
                                           command=( lambda : select_file_in_Download_From_a_File( ret_mgmt, main_mgmt ) ) )
    ret_mgmt['select_button'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['see_info_button'] = tk.Button( ret_mgmt['up_frame'], text='See Information',
                                             command=( lambda : see_info_in_Download_From_a_File( ret_mgmt, main_mgmt ) ) )
    ret_mgmt['see_info_button'].pack( side=tk.LEFT, padx=5 )

    ### set on "ret_mgmt['down_frame']"  ### add frame

    ret_mgmt['filter_frame'] = tk.Frame( ret_mgmt['down_frame'], height=50 )
    ret_mgmt['filter_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y )

    ret_mgmt['display_frame'] = tk.Frame( ret_mgmt['down_frame'] )
    ret_mgmt['display_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y )

    ### set on "ret_mgmt['filter_frame']"

    data['input_opt_default_dict'] = { 'itag' : 18, 
                                       'type' : 'video', 
                                       'subtype' : 'mp4', 
                                       'res' : '720p', 
                                       'abr' : '128kbps',
                                       'caption' : 'zh-Hant' }

    ret_mgmt['chk_val_dict'] = { 
        'filter_dict' : { 'itag' : tk.BooleanVar( value=False ),
                          'highest' : tk.BooleanVar( value=False ),
                          'type' : tk.BooleanVar( value=False ),
                          'subtype' : tk.BooleanVar( value=False ),
                          'res' : tk.BooleanVar( value=False ),
                          'abr' : tk.BooleanVar( value=False ),
                          'only_audio' : tk.BooleanVar( value=False ),
                          'only_video' : tk.BooleanVar( value=False ),
                          'progressive' : tk.BooleanVar( value=False ) },
        'caption' : tk.BooleanVar( value=False ),
        'only_caption' : tk.BooleanVar( value=False ) }
    
    for key in ret_mgmt['chk_val_dict']['filter_dict'].keys() :

        ret_mgmt[key] = tk.Checkbutton( ret_mgmt['filter_frame'], text=key,
                                        var=ret_mgmt['chk_val_dict']['filter_dict'][key] ) 
        ret_mgmt[key].pack( pady=1, anchor=tk.NW )

        if key in data['input_opt_default_dict'].keys() :
            ret_mgmt[key + '_strVar'] = tk.StringVar( value=data['input_opt_default_dict'][key] )
            ret_mgmt[key + '_entry'] = tk.Entry( ret_mgmt['filter_frame'], textvariable=ret_mgmt[key + '_strVar'], width=15 )
            ret_mgmt[key + '_entry'].pack( padx=20, anchor=tk.NW )

    ret_mgmt['caption'] = tk.Checkbutton( ret_mgmt['filter_frame'], text='caption',
                                          var=ret_mgmt['chk_val_dict']['caption'] ) 
    ret_mgmt['caption'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['caption_strVar'] = tk.StringVar( value=data['input_opt_default_dict']['caption'] )
    ret_mgmt['caption_entry'] = tk.Entry( ret_mgmt['filter_frame'], textvariable=ret_mgmt['caption_strVar'], width=15 )
    ret_mgmt['caption_entry'].pack( padx=20, anchor=tk.NW )

    ret_mgmt['only_caption'] = tk.Checkbutton( ret_mgmt['filter_frame'], text='only_caption',
                                               var=ret_mgmt['chk_val_dict']['only_caption'] ) 
    ret_mgmt['only_caption'].pack( pady=5, anchor=tk.NW )

    ret_mgmt['chk_val_dict']['filter_dict']['itag'].trace( 'w', lambda arg1, arg2, arg3 : 
                                                           check_ability_in_Download_From_a_File( ret_mgmt ) ) ## monitor
    ret_mgmt['chk_val_dict']['filter_dict']['highest'].trace( 'w', lambda arg1, arg2, arg3 :
                                                              check_ability_in_Download_From_a_File( ret_mgmt ) ) ## monitor
    ret_mgmt['chk_val_dict']['only_caption'].trace( 'w', lambda arg1, arg2, arg3 :
                                                    check_ability_in_Download_From_a_File( ret_mgmt ) ) ## monitor

    ### set on "ret_mgmt['display_frame']"  ### add frame

    ret_mgmt['action_frame'] = tk.Frame( ret_mgmt['display_frame'] )
    ret_mgmt['action_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['info_frame'] = tk.Frame( ret_mgmt['display_frame'] )
    ret_mgmt['info_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ### set on "ret_mgmt['action_frame']"

    ret_mgmt['download_button'] = tk.Button( ret_mgmt['action_frame'], text='Download', bg='yellow',
                                             command=( lambda : download_in_Download_From_a_File( ret_mgmt, main_mgmt, data ) ) )
    ret_mgmt['download_button'].pack( side=tk.LEFT, padx=30 )

    ret_mgmt['download_warning_label'] = tk.Label( ret_mgmt['action_frame'], text='', fg='red' )

    ### set on "ret_mgmt['info_frame']"

    ret_mgmt['info_label'] = tk.Label( ret_mgmt['info_frame'], text='Information :' )
    ret_mgmt['info_label'].pack( padx=30, pady=5, anchor=tk.NW )

    ret_mgmt['show_info_text'] = tkscrolled.ScrolledText( ret_mgmt['info_frame'], width=120, height=50, state=tk.DISABLED )
    ret_mgmt['show_info_text'].pack( padx=30, anchor=tk.NW )

    return ret_mgmt




