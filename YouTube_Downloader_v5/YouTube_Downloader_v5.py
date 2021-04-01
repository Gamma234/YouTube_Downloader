
import tkinter as tk
import os
import shutil

from data.tools.Global_Tools import Global_Tools as GT
from data.tools.YouTube_DLer_v5 import YouTube_Downloader as YTDL
from data.tools.YouTube_DLer_v5 import Audio_Video_Handler as AVHD

from data.tools.Print_Information import *
from data.tools.Single_Download import *
from data.tools.Create_an_IP_File import *
from data.tools.Download_From_a_File import *
from data.tools.Download_From_a_Playlist import *
from data.tools.Combine_an_audio_stream_and_a_video_stream import *
from data.tools.Combine_several_audio_files_and_video_files import *

class YouTube_Downloader_GUI_System() :

    def __init__( self ) :

        if os.path.exists( 'combine_temp_workplace' ) :
             shutil.rmtree( 'combine_temp_workplace' )

        self.mgmt = {} ## empty dictionary
        self.conf = {} ## empty dictionary
        self.temp = None

        self.mgmt['main_window'] = tk.Tk()
        self.conf['main_width'] = 1000
        self.conf['main_height'] = 600

        self.mgmt['main_window'].geometry( str(self.conf['main_width']) + 'x' + str(self.conf['main_height']) )
        self.mgmt['main_window'].title( 'YouTube Video Downloader' )
        self.mgmt['main_window'].resizable( False, False )

        ### set on "self.mgmt['main_window']"

        self.mgmt['left_frame'] = tk.Frame( self.mgmt['main_window'] )
        self.mgmt['left_frame'].pack( side=tk.LEFT, fill=tk.Y )

        boundary_line = tk.Canvas( self.mgmt['main_window'], background='black', width=5 )
        boundary_line.pack( side=tk.LEFT, fill=tk.Y )

        self.mgmt['right_frame'] = tk.Frame( self.mgmt['main_window'] )
        self.mgmt['right_frame'].pack( side=tk.LEFT, fill=tk.Y )

        ### set on "self.mgmt['left_frame']"

        self.mgmt['status_frame'] = tk.Frame( self.mgmt['left_frame'] )
        self.mgmt['status_frame'].pack( side=tk.TOP, fill=tk.BOTH )

        boundary_line = tk.Canvas( self.mgmt['left_frame'], width=5, height=5 )
        boundary_line.pack( side=tk.TOP, fill=tk.X )

        self.mgmt['options_frame'] = tk.Frame( self.mgmt['left_frame'], background='#A8776D' )
        self.mgmt['options_frame'].pack( side=tk.TOP, fill=tk.BOTH, expand=tk.YES )

    def add_status( self ) :

        ### set on "self.mgmt['status_frame']"
        
        self.mgmt['save_path_label'] = tk.Label( self.mgmt['status_frame'], text='Save Path' )
        self.mgmt['save_path_label'].pack( side=tk.TOP )

        self.mgmt['save_path_strVar'] = tk.StringVar()
        self.mgmt['save_path_entry'] = tk.Entry( self.mgmt['status_frame'], textvariable=self.mgmt['save_path_strVar'],
                                                 highlightthickness=2, highlightbackground='green', highlightcolor='green' )
        self.mgmt['save_path_entry'].pack( side=tk.TOP )
        
        self.mgmt['download_label'] = tk.Label( self.mgmt['status_frame'], text='Download' )
        self.mgmt['download_label'].pack( side=tk.TOP )

        self.mgmt['download_frame'] = tk.Frame( self.mgmt['status_frame'] )
        self.mgmt['download_frame'].pack( side=tk.TOP )

        ### set on "self.mgmt['download_frame']"

        self.mgmt['download_boolVar'] = tk.BooleanVar( value=True )

        self.mgmt['download_on'] = tk.Button( self.mgmt['download_frame'], text='ON', background='SystemButtonFace',
                                              command=( lambda : self.change_download_status( 'ON' ) ) )
        self.mgmt['download_on'].pack( side=tk.LEFT, padx=5 )

        self.mgmt['download_off'] = tk.Button( self.mgmt['download_frame'], text='OFF', background='grey',
                                               command=( lambda : self.change_download_status( 'OFF' ) ) )
        self.mgmt['download_off'].pack( side=tk.LEFT, padx=5 )

    def add_options_button( self ) :

        ### set on "self.mgmt['options_frame']"

        options_dict = { 'Print Information' : None,
                         'Single Download' : None,
                         'Create an IP File' : None,
                         'Download From a File' : None,
                         'Download From a Playlist' : None,
                         'Combine an audio stream\n and a video stream' : None,
                         'Combine several audio files\n and video files' : None }

        options_func = [ Print_Information, 
                         Single_Download, 
                         Create_an_IP_File, 
                         Download_From_a_File, 
                         Download_From_a_Playlist,
                         Combine_an_audio_stream_and_a_video_stream, 
                         Combine_several_audio_files_and_video_files ]

        for i, key in enumerate( options_dict.keys() ) :
            options_dict[key] = tk.Button( self.mgmt['options_frame'], text=key,
                                           command=( lambda func=options_func[i] : self.do_option( func ) ) )
            options_dict[key].pack( padx=5, pady=5, anchor=tk.NW )

    def set_save_path( self, new_save_path ) :

        save_path_file = open( 'data\\save_path.txt', 'w' )
        save_path_file.write( new_save_path )
        save_path_file.close()

    def add_save_path( self ) :

        try :
            save_path_file = open( 'data\\save_path.txt', 'r' )
            save_path = save_path_file.readline()
            self.mgmt['save_path_strVar'].set( save_path )

            if save_path != '' and ( not os.path.exists( save_path ) ) :
                self.mgmt['save_path_entry'].config( highlightbackground='red', highlightcolor='red' )                    

            save_path_file.close()
        except Exception as e :
            self.mgmt['save_path_strVar'].set( '"data\\save_path.txt" not exist !' )
            self.mgmt['save_path_entry'].config( highlightbackground='red', highlightcolor='red' )

    def check_save_path( self, *args ) :

        save_path = self.mgmt['save_path_entry'].get()

        if self.mgmt['save_path_entry']['highlightbackground'] == 'green' :
            if save_path == '' or os.path.isdir( save_path ) :
                pass
            else :
                self.mgmt['save_path_entry'].config( highlightbackground='red', highlightcolor='red' )
        else :
            if save_path == '' or os.path.isdir( save_path ) :
                self.set_save_path( save_path )
                self.mgmt['save_path_entry'].config( highlightbackground='green', highlightcolor='green' )
            else :
                pass

    def run( self ):

        ### add basic objects

        self.add_status()
        self.add_options_button()
        self.add_save_path()

        ### add monitor

        self.mgmt['save_path_strVar'].trace( 'w', self.check_save_path )

        ### run

        self.mgmt['main_window'].mainloop()

    def do_option( self, func ) :

        if func == None :
            return
        else :
            if self.temp != None :
                GT.all_destroy( self.temp )
            self.temp = func( self.mgmt['right_frame'], self.mgmt, self.conf )            

    def change_download_status( self, button ) :

        if ( ( button == 'ON' and self.mgmt['download_boolVar'].get() == True ) or
             ( button == 'OFF' and self.mgmt['download_boolVar'].get() == False ) ) :
            return

        self.mgmt['download_boolVar'].set( not self.mgmt['download_boolVar'].get() )

        if self.mgmt['download_boolVar'].get() == True :
            self.mgmt['download_on'].config( bg='SystemButtonFace' )
            self.mgmt['download_off'].config( bg='grey' )
        else :
            self.mgmt['download_on'].config( bg='grey' )
            self.mgmt['download_off'].config( bg='SystemButtonFace' )
            
if True and __name__ == "__main__":

    ydlgs = YouTube_Downloader_GUI_System()
    ydlgs.run()



