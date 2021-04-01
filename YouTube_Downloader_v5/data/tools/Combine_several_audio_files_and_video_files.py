
from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL
from data.tools.YouTube_DLer_v5 import Audio_Video_Handler as AVHD

import tkinter.scrolledtext as tkscrolled
import tkinter.filedialog as filedlg
import tkinter as tk
import os

def handle_combine_in_Combine_several_audio_files_and_video_files( audio_files, video_files, mgmt, main_mgmt ) :

    done_num, fail_num = 0, 0

    for i in range( len( video_files ) ) :

        GT.write_text( mgmt['action_info_text'], ( '[' + str(i + 1) + ']\n\n' + video_files[i] + '\n' + audio_files[i] + '\n\n' ),
                       fg='SystemWindowText', replace=False, to_bottom=True )
        main_mgmt['main_window'].update()

        try :
            AVHD.combine_audio_video_file( video_file_name = mgmt['video_strVar'].get() + '/' + video_files[i], 
                                           audio_file_name = mgmt['audio_strVar'].get() + '/' + audio_files[i], 
                                           title=video_files[i].split( '.' )[0], 
                                           save_path=main_mgmt['save_path_strVar'].get() )
            GT.write_text( mgmt['action_info_text'], 'Done\n\n\n',
                           fg='SystemWindowText', replace=False, to_bottom=True )
            done_num += 1
        except Exception as e :
            GT.write_text( mgmt['action_info_text'], ( 'Fail (' + str(e) + ')\n\n\n' ),
                           fg='SystemWindowText', replace=False, to_bottom=True )
            fail_num += 1 

        main_mgmt['main_window'].update()
    
    mgmt['action_warning_label'].config( text=( 'Done : ' + str( done_num ) + '\n' + 'Fail : ' + str( fail_num ) ), fg='green' )
    mgmt['action_warning_label'].pack( padx=20, pady=5, anchor=tk.NW )

def combine_in_Combine_several_audio_files_and_video_files( mgmt, main_mgmt ) :

    mgmt['action_warning_label'].pack_forget()
    mgmt['action_button'].config( state=tk.DISABLED )
    GT.write_text( mgmt['action_info_text'], '', fg='SystemWindowText' )

    try :
        running = True

        if running and main_mgmt['download_boolVar'].get() == False :
            GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'Download OFF', fg='red' )
            mgmt['action_warning_label'].pack_forget()
            running = False

        if running and main_mgmt['save_path_entry']['highlightbackground'] != 'green' :
            GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'Invalid Save Path', fg='red' )
            mgmt['action_warning_label'].pack_forget()
            running = False

        if running and mgmt['audio_entry']['highlightbackground'] != 'green' :
            GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'Invalid Audio Path', fg='red' )
            mgmt['action_warning_label'].pack_forget()
            running = False

        if running and mgmt['video_entry']['highlightbackground'] != 'green' :
            GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'Invalid Video Path', fg='red' )
            mgmt['action_warning_label'].pack_forget()
            running = False

        if running :
            audio_files = os.listdir( mgmt['audio_strVar'].get() )
            video_files = os.listdir( mgmt['video_strVar'].get() )

            if len( audio_files ) != len( video_files ) :
                GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'File numbers are not equal !', fg='red' )
                mgmt['action_warning_label'].pack_forget()
                running = False

            if running and all( video_files[i].split( '.' )[0] == audio_files[i].split( '.' )[0]
                                for i in range( len( video_files ) ) ) == False :
                GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + 'Without own extension, some file names are not equal !', fg='red' )
                mgmt['action_warning_label'].pack_forget()
                running = False

            if running :
                handle_combine_in_Combine_several_audio_files_and_video_files( audio_files, video_files, mgmt, main_mgmt )

    except Exception as e :
        GT.write_text( mgmt['action_info_text'], '[ERROR]\n' + str( e ), fg='red' )
        mgmt['action_warning_label'].pack_forget()

    ## wait 200 ms to do the lambda
    main_mgmt['main_window'].after( 200, lambda : mgmt['action_button'].config( state=tk.NORMAL ) ) 

def check_path_in_Combine_several_audio_files_and_video_files( mgmt, strVar, entry, text ) :

    def write_dir( mgmt, text, dir_list ) :
        msg = ''
        for i in range( len( dir_list ) ) :
            msg = msg + '[' + str(i + 1) + '] ' + dir_list[i] + '\n'
        GT.write_text( text_window=mgmt[text], msg=msg )

    if mgmt[entry]['highlightbackground'] == 'green' :
        if os.path.isdir( mgmt[strVar].get() ) :
            write_dir( mgmt, text, os.listdir( mgmt[strVar].get() ) )
        else :
            mgmt[entry].config( highlightbackground='red', highlightcolor='red' )
            GT.write_text( text_window=mgmt[text], msg='' )
    else :
        if os.path.isdir( mgmt[strVar].get() ) :
            mgmt[entry].config( highlightbackground='green', highlightcolor='green' )
            write_dir( mgmt, text, os.listdir( mgmt[strVar].get() ) )
        else :
            GT.write_text( text_window=mgmt[text], msg='' )

def select_path_in_Combine_several_audio_files_and_video_files( mgmt, strVar, entry ) :

    mgmt[strVar].set( filedlg.askdirectory() )
    mgmt[entry].xview( tk.END )

def Combine_several_audio_files_and_video_files( main_frame, main_mgmt, main_conf ) :
    
    ret_mgmt = {} ## empty dictionary

    ### add frame

    ret_mgmt['audio_input_frame'] = tk.Frame( main_frame )
    ret_mgmt['audio_input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )

    ret_mgmt['video_input_frame'] = tk.Frame( main_frame )
    ret_mgmt['video_input_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )   
    
    ret_mgmt['info_frame'] = tk.Frame( main_frame )
    ret_mgmt['info_frame'].pack( side=tk.TOP, pady=20, fill=tk.X )

    ret_mgmt['action_frame'] = tk.Frame( main_frame )
    ret_mgmt['action_frame'].pack( side=tk.TOP, pady=5, fill=tk.X )  

    ### set on "ret_mgmt['audio_input_frame']"

    ret_mgmt['audio_label'] = tk.Label( ret_mgmt['audio_input_frame'], text='Audio Files Path :' )
    ret_mgmt['audio_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['audio_strVar'] = tk.StringVar()
    ret_mgmt['audio_strVar'].set( '' )

    ret_mgmt['audio_entry'] = ( tk.Entry( ret_mgmt['audio_input_frame'], width=70, textvariable=ret_mgmt['audio_strVar'],
                                          highlightthickness=2, highlightbackground='green', highlightcolor='green' ) 
                                if os.path.isdir( ret_mgmt['audio_strVar'].get() ) else
                                tk.Entry( ret_mgmt['audio_input_frame'], width=70, textvariable=ret_mgmt['audio_strVar'],
                                          highlightthickness=2, highlightbackground='red', highlightcolor='red' ) )
    ret_mgmt['audio_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['audio_strVar'].trace( 'w', lambda arg1, arg2, arg3 : check_path_in_Combine_several_audio_files_and_video_files( ret_mgmt,
                                                                                                                              'audio_strVar',
                                                                                                                              'audio_entry',
                                                                                                                              'audio_info_text' ) ) ## monitor

    ret_mgmt['audio_button'] = tk.Button( ret_mgmt['audio_input_frame'], text='Select Path',
                                          command=( lambda : select_path_in_Combine_several_audio_files_and_video_files( ret_mgmt, 'audio_strVar', 'audio_entry' ) ) )
    ret_mgmt['audio_button'].pack( side=tk.LEFT, padx=5 )

    ### set on "ret_mgmt['video_input_frame']"

    ret_mgmt['video_label'] = tk.Label( ret_mgmt['video_input_frame'], text='Video Files Path :' )
    ret_mgmt['video_label'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['video_strVar'] = tk.StringVar()
    ret_mgmt['video_strVar'].set( '' )

    ret_mgmt['video_entry'] = ( tk.Entry( ret_mgmt['video_input_frame'], width=70, textvariable=ret_mgmt['video_strVar'],
                                          highlightthickness=2, highlightbackground='green', highlightcolor='green' ) 
                                if os.path.isdir( ret_mgmt['video_strVar'].get() ) else
                                tk.Entry( ret_mgmt['video_input_frame'], width=70, textvariable=ret_mgmt['video_strVar'],
                                          highlightthickness=2, highlightbackground='red', highlightcolor='red' ) )
    ret_mgmt['video_entry'].pack( side=tk.LEFT, padx=5 )

    ret_mgmt['video_strVar'].trace( 'w', lambda arg1, arg2, arg3 : check_path_in_Combine_several_audio_files_and_video_files( ret_mgmt,
                                                                                                                              'video_strVar',
                                                                                                                              'video_entry',
                                                                                                                              'video_info_text' ) ) ## monitor

    ret_mgmt['video_button'] = tk.Button( ret_mgmt['video_input_frame'], text='Select Path',
                                          command=( lambda : select_path_in_Combine_several_audio_files_and_video_files( ret_mgmt, 'video_strVar', 'video_entry' ) ) )
    ret_mgmt['video_button'].pack( side=tk.LEFT, padx=5 )

    ### set on "ret_mgmt['info_frame']"  ### add frame

    ret_mgmt['audio_info_frame'] = tk.Frame( ret_mgmt['info_frame'] )
    ret_mgmt['audio_info_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y )

    ret_mgmt['video_info_frame'] = tk.Frame( ret_mgmt['info_frame'] )
    ret_mgmt['video_info_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y ) 

    ### set on "ret_mgmt['audio_info_frame']"

    ret_mgmt['audio_info_label'] = tk.Label( ret_mgmt['audio_info_frame'], text='Audio Files :' )
    ret_mgmt['audio_info_label'].pack( padx=5, pady=5, anchor=tk.NW )

    ret_mgmt['audio_info_text'] = tkscrolled.ScrolledText( ret_mgmt['audio_info_frame'], width=50, height=15, state=tk.DISABLED )
    ret_mgmt['audio_info_text'].pack( padx=10, anchor=tk.NW )

    ### set on "ret_mgmt['video_info_frame']"

    ret_mgmt['video_info_label'] = tk.Label( ret_mgmt['video_info_frame'], text='Video Files :' )
    ret_mgmt['video_info_label'].pack( padx=5, pady=5, anchor=tk.NW )

    ret_mgmt['video_info_text'] = tkscrolled.ScrolledText( ret_mgmt['video_info_frame'], width=50, height=15, state=tk.DISABLED )
    ret_mgmt['video_info_text'].pack( padx=10, anchor=tk.NW )

    ### set on "ret_mgmt['action_frame']"  ### add frame

    ret_mgmt['action_opt_frame'] = tk.Frame( ret_mgmt['action_frame'] )
    ret_mgmt['action_opt_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y )

    ret_mgmt['action_info_frame'] = tk.Frame( ret_mgmt['action_frame'] )
    ret_mgmt['action_info_frame'].pack( side=tk.LEFT, padx=5, fill=tk.Y ) 

    ### set on "ret_mgmt['action_opt_frame']"

    ret_mgmt['action_button'] = tk.Button( ret_mgmt['action_opt_frame'], text='Combine', bg='yellow',
                                           command=( lambda : combine_in_Combine_several_audio_files_and_video_files( ret_mgmt, main_mgmt ) ) )
    ret_mgmt['action_button'].pack( padx=20, pady=5, anchor=tk.NW )

    ret_mgmt['action_warning_label'] = tk.Label( ret_mgmt['action_opt_frame'], text='', fg='red' )

    ### set on "ret_mgmt['action_info_frame']"

    ret_mgmt['action_info_label'] = tk.Label( ret_mgmt['action_info_frame'], text='Information :' )
    ret_mgmt['action_info_label'].pack( padx=5, pady=5, anchor=tk.NW )

    ret_mgmt['action_info_text'] = tkscrolled.ScrolledText( ret_mgmt['action_info_frame'], width=90, height=15, state=tk.DISABLED )
    ret_mgmt['action_info_text'].pack( padx=10, anchor=tk.NW )

    return ret_mgmt




