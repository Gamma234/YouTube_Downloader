
from data.tool.YouTube_DLer_v4 import *
import os

class YouTube_Downloader_System() :

    def __init__( self ) :
        self.save_path = self.get_save_path()
        self.ytdl = YouTube_Downloader( save_path=self.save_path )

        if not os.path.exists( self.save_path ) :
            print( 'ERROR : The initial save path does not exist !' )
            print( '        Set a new save path.', end='\n\n' )
            self.save_path = None
            self.run_option_8()

        self.download = True

    def get_save_path( self ) :

        save_path = ''

        try :
            save_path_file = open( 'data\\save_path.txt', 'r' )
            save_path = save_path_file.readline()
            save_path_file.close()
        except Exception as e :
            print( str( e ), end='\n\n' )

        return save_path

    def set_save_path( self, new_save_path ) :

        try :
            save_path_file = open( 'data\\save_path.txt', 'w' )
            save_path_file.write( new_save_path )
            save_path_file.close()
        except Exception as e :
            print( str( e ), end='\n\n' )

    def get_int( self, statement='' ) :

        while True :
            try :
                num = int( input( statement ) )
                print( 'Get your input :', num, end='\n\n' )
                return num
            except :
                print( 'ERROR : Wrong input !', end='\n\n' )  

    def get_option( self ) :
        
        print( '===== Setting ===================' )
        print( 'save path :', self.save_path )
        print( 'download :', 'Open' if self.download else 'Close' )
        print( '===== Options ===================' )
        print( '0. Quit' )
        print( '1. Print Information' ) ## url
        print( '2. Single Download' ) ## url
        print( '3. Create an IP File' ) ## playlist_url
        print( '4. Download From a File' ) ## ip_file_name
        print( '5. Download From a Playlist' ) ## playlist_url
        print( '6. Combine an audio stream and a video stream' )
        print( '7. Combine several audio files and video files' )
        print( '8. Change the "save path"' )
        print( '9. Open/Close "download"' )
        print( '=================================', end='\n\n' )

        return self.get_int( '>>> Input an option : ' )

    def run( self ) :

        running = True

        while running :

            option = self.get_option()

            try:
                if option == 0 : ## Quit
                    running = False
                elif option == 1 : ## Print Information
                    self.run_option_1()
                elif option == 2 : ## Single Download
                    self.run_option_2()
                elif option == 3 : ## Create an IP File
                    self.run_option_3()
                elif option == 4 : ## Download From a File
                    self.run_option_4()
                elif option == 5 : ## Download From a Playlist
                    self.run_option_5()
                elif option == 6 : ## Combine an audio stream and a video stream
                    self.run_option_6()
                elif option == 7 : ## Combine several audio files and video files
                    self.run_option_7()
                elif option == 8 : ## Change the "save path"
                    self.run_option_8()
                elif option == 9 : ## Open/Close "download"
                    self.run_option_9()
                else :
                    print(  'ERROR : The option does not exist !', end='\n\n'  )
            except Exception as e :
                print( str( e ), end='\n\n' )
            print( '=================================', end='\n\n' )

    def run_option_1( self ) : ## Print Information
        print( '===== Get Information ===========', end='\n\n' )

        try :
            url = input( '>>> Input URL : ' )
            print()

            self.ytdl.print_information( url=url )
        except Exception as e :
            raise e

    def run_option_2( self ) : ## Single Download
        print( '===== Single Download ===========', end='\n\n' )

        try :
            url = input( '>>> Input URL : ' )
            print( '\nSee information below :', end='\n\n' )

            self.ytdl.print_information( url=url )

            itag = input( '>>> Choose an "itag" to download : ' )
            language_code = input( '>>> Input a language code ( 0 for not download ) : ' )
            print()

            if language_code == '0' or language_code == '' :
                self.ytdl.single_download( url, itag, download=self.download )
            else :
                self.ytdl.single_download( url, itag, download=self.download, language_code=language_code )
        except Exception as e :
            raise e

    def run_option_3( self ) : ## Create an IP File
        print( '===== Create an IP File ==========', end='\n\n' )

        try :
            playlist_url = input( '>>> Input playlist URL : ' )
            file_name = input( '>>> Input file name ( 0 for ip_file.txt ) : ' )
            print()

            if file_name == '0' or file_name == '' :
                self.ytdl.create_ip_file( playlist_url )
            else :
                self.ytdl.create_ip_file( playlist_url, file_name=file_name )
        except Exception as e :
            raise e

    def run_option_4( self ) : ## Download From a File
        print( '===== Download From a File ======', end='\n\n' )

        try :
            ip_file_name = input( '>>> Input file name ( 0 for ip_file.txt ) : ' )

            if ip_file_name == '0' or ip_file_name == '' :
                ip_file_name = 'ip_file.txt'

            language_code = input( '>>> Input a language code ( 0 for not download ) : ' )
            print()

            filter_dic = None

            while True :
                print( 'Current filter_dic :\n', filter_dic, end='\n\n' )
                set_fd = input( '>>> Set filter_dic ? ( y for yes, others for no ) : ' )
                print()
                if set_fd.lower() == "y" or set_fd.lower() == "yes" :
                    filter_dic = self.set_filter_dic( filter_dic )
                else :
                    break

            if language_code == '0' or language_code == '' :
                self.ytdl.download_from_file( ip_file_name, download=self.download, filter_dic=filter_dic )
            else :
                self.ytdl.download_from_file( ip_file_name, download=self.download, language_code=language_code,
                                              filter_dic=filter_dic )
        except Exception as e :
            raise e

    def run_option_5( self ) : ## Download From a Playlist
        print( '===== Download From a Playlist ==', end='\n\n' )

        try :
            playlist_url = input( '>>> Input playlist URL : ' )
            language_code = input( '>>> Input a language code ( 0 for not download ) : ' )
            limit_num = self.get_int( '>>> Input a limit num ( 0 for no limit ) : ' )
            print()

            if limit_num <= 0 :
                limit_num = None

            filter_dic = None

            while True :
                print( 'Current filter_dic :\n', filter_dic, end='\n\n' )
                set_fd = input( '>>> Set filter_dic ? ( y for yes, others for no ) : ' )
                print()
                if set_fd.lower() == "y" or set_fd.lower() == "yes" :
                    filter_dic = self.set_filter_dic( filter_dic )
                else :
                    break

            if language_code == '0' or language_code == '' :
                self.ytdl.playlist_download( playlist_url, download=self.download, filter_dic=filter_dic,
                                             limit_num=limit_num )
            else :
                self.ytdl.playlist_download( playlist_url, download=self.download, language_code=language_code,
                                             filter_dic=filter_dic, limit_num=limit_num )
        except Exception as e :
            raise e

    def run_option_6( self ) : ## Combine an audio stream and a video stream
        print( '===== Combine an audio stream and a video stream ===================', end='\n\n' )

        try :
            url = input( '>>> Input URL : ' )
            print( '\nSee information below :', end='\n\n' )

            self.ytdl.print_information( url=url, show_details=False, show_subtitle=True, show_stream=False,
                                         only_audio=True, only_video=True, show_progressive=False )

            audio_itag = input( '>>> Choose an "audio itag" : ' )
            video_itag = input( '>>> Choose an "video itag" : ' )
            language_code = input( '>>> Input a language code ( 0 for not download ) : ' )
            print()

            if language_code == '0' or language_code == '' :
                self.ytdl.download_single_video_audio_combine( url=url, audio_itag=audio_itag, video_itag=video_itag,
                                                               download=self.download )
            else :
                self.ytdl.download_single_video_audio_combine( url=url, audio_itag=audio_itag, video_itag=video_itag,
                                                               download=self.download, language_code=language_code )
        except Exception as e :
            raise e

    def run_option_7( self ) : ## Combine several audio files and video files
        print( '===== Combine several audio files and video files ==================', end='\n\n' )

        try :
            video_files_path = input( '>>> Input the video files path : ' )
            audio_files_path = input( '>>> Input the audio files path : ' )
            print()

            self.ytdl.multi_video_audio_combine( video_files_path, audio_files_path )
        except Exception as e :
            raise e

    def run_option_8( self ) : ## Change the "save path"
        print( '===== Change the "save path" ====', end='\n\n' )

        try :
            print( 'Current "save path" :', self.save_path, end='\n\n' )

            new_save_path = ''

            while True :
                new_save_path = input( '>>> Input a new "save path" : ' )
                if os.path.exists( new_save_path ) :
                    print( 'New "save path" :', new_save_path, end='\n\n' )
                    break
                else :
                    print( 'ERROR : The path does not exist !', end='\n\n' )
        
            self.set_save_path( new_save_path )
            self.save_path = self.get_save_path()
            self.ytdl = YouTube_Downloader( save_path=self.save_path )
        except Exception as e :
            raise e

    def run_option_9( self ) : ## Open/Close "download"
        print( '===== Open/Close "download" =====', end='\n\n' )

        try :
            self.download = not self.download

            print( 'Change "download" :', 'Open' if not self.download else 'Close', '->',
                                          'Open' if self.download else 'Close', end='\n\n' )
        except Exception as e :
            raise e

    def set_filter_dic( self, filter_dic ) :

        while True :

            print( '------Current filter_dic---------' )
            print( filter_dic )
            print( '------Options--------------------' )
            print( '0. Done' )
            print( '1. Clear' )
            print( '2. Input Setting' ) 
            print( '---------------------------------', end='\n\n' )

            option = self.get_int( '>>> Input an option : ' )

            if option == 0 :
                break
            elif option == 1 :
                filter_dic = None
            elif option == 2 :
                filter_dic = self.set_filter_dic_option_2()
            else :
                print( 'ERROR : The option does not exist !', end='\n\n'  )

        return filter_dic

    def set_filter_dic_option_2( self ) :

        filter_dic = { "type" : None, "subtype" : None, "res" : None, "fps" : None, "abr" : None,
                       "only_audio" : None, "only_video" : None, "progressive" : None }

        alias_dic = { "t" : 'type', "st" : 'subtype', "r" : 'res', "f" : 'fps', "a" : 'abr',
                      "oa" : 'only_audio', "ov" : 'only_video', "p" : 'progressive' }

        print( '------Introduction---------------' )
        print( 'type        (t)  = None | "video" | "audio"' )
        print( 'subtype     (st) = None | "mp4" | ...' )
        print( 'res         (r)  = None | "1080p" | "720p" | ...' )
        print( 'fps         (f)  = None | "30fps" | ...' )
        print( 'abr         (a)  = None | "128kbps" | "50kbps" | ...' )        
        print( 'only_audio  (oa) = None | True | False' )
        print( 'only_video  (ov) = None | True | False' )
        print( 'progressive (p)  = None | True | False' )
        print( '------Example--------------------' )
        print( 'st = mp4, r = 720p, p = True' )
        print( '---------------------------------', end='\n\n' )

        setting = re.sub( '[ \t]', '', input( '>>> Input setting : ' ) ) ## input and remove white spaces
        setting = [ s.split( '=' ) for s in setting.lower().split( ',' ) ]

        for s in setting :
            if ( len( s ) == 2 ) and ( s[0] in alias_dic.keys() ) :
                if s[0] in ['oa', 'ov', 'p'] :
                    if s[1] == 'true' or s[1] == 't' :
                        filter_dic[alias_dic[s[0]]] = True
                    elif s[1] == 'false' or s[1] == 'f' :
                        filter_dic[alias_dic[s[0]]] = False
                    else :
                        filter_dic[alias_dic[s[0]]] = None
                else :
                    if s[1] == 'none' :
                        filter_dic[alias_dic[s[0]]] = None
                    else :
                        filter_dic[alias_dic[s[0]]] = s[1]

        if all( v == None for v in filter_dic.values() ) : ## if all None, then set filter_dic to None
            filter_dic = None

        return filter_dic

ydls = YouTube_Downloader_System()
ydls.run()



